# import requests
# from ollama import chat

# urls = [
#    "https://twitter.com/moneycontrolcom/status/1981226445004558384"
# ]
# html_response = requests.get("https://x.com/moneycontrolcom")
# html_text = html_response.content
# print(html_text)



import os
import time
from ollama import chat, web_fetch
from pydantic import BaseModel, ValidationError
import json
import pandas as pd

os.environ["OLLAMA_API_KEY"] = "4d169e51df3c4acd9ceffc25a9798ecc.SzxaICfxVVvaMFg1iaUBuwUF"

file = pd.ExcelFile(r'D:\PythonScripts\AuthorNameAXIS\Untitled spreadsheet.xlsx')
file_data = file.parse('23 Oct - 28 Oct')
file_data = file_data[file_data['Resource type'] == 'Mass media']

urls = list(file_data['URL'])

class ArticleInfo(BaseModel):
    title: str
    author: str | None = None
    confidence: int  # confidence percentage from 0 to 100

def fetch_and_extract(url):
    article = web_fetch(url)
    
    prompt = f"""
Below is a news article and its HTML source.

Extract these fields in JSON format:

- title: The article title
- author: The author's name or published by name found in the text or HTML meta tags
- confidence: Your confidence in the author name's accuracy as a percentage from 0 to 100

**Author Extraction Guidelines:**
1. First, check HTML meta tags (author, byline, publisher) and structured data
2. If no author found in metadata, scan the article body for contextual clues:
   - Look for phrases like "press release provided by", "published by", "source:", or similar attribution statements
   - Identify corporate/organizational sources mentioned as content providers
   - Note disclaimers about content origin
3. Return null for author ONLY if no credible source can be identified
4. If an organizational source is found (like "VMPL" in press releases), use that as the author
5. Ignore names of people quoted, experts mentioned, or interviewees
6. Distinguish between content creators and content subjects

**Confidence Scoring:**
- 90-100%: Author name found in reliable metadata (meta tags, structured data)
- 70-89%: Clear organizational attribution in article body (press release sources)
- 50-69%: Indirect references or partial attribution
- 1-49%: Weak or inferred attribution
- 0%: No author information whatsoever

Return ONLY valid JSON matching this schema:

  "title": "string",
  "author": "string or null", 
  "confidence": "number"

ARTICLE CONTENT:
{article.content}
    """

    response = chat(
        model="",
        messages=[{"role": "user", "content": prompt}],
        format=ArticleInfo.model_json_schema()
    )
    return response.message.content

max_retries = 5
delay_between_requests = 2  # seconds
backoff_time = 30  # seconds; initial backoff on rate limit

for idx, url in enumerate(urls, 1):
    retries = 0
    while retries < max_retries:
        try:
            json_response = fetch_and_extract(url)
            article_info = ArticleInfo.model_validate_json(json_response)
            print(json.dumps(article_info.model_dump(), indent=2, ensure_ascii=False))
            time.sleep(delay_between_requests)
            break  # exit retry loop if success
        except ValidationError as e:
            print(f"Validation failed for URL {url}: {e}")
            break  # skip to next URL
        except Exception as e:
            # Check if error is rate limiting (insert your error type check as per Ollama's SDK)
            if "rate limit" in str(e).lower():
                print(f"Rate limit hit at URL {url}, retrying after backoff {backoff_time} seconds...")
                time.sleep(backoff_time)
                retries += 1
                backoff_time *= 2  # exponential backoff
            else:
                print(f"Error fetching data for URL {url}: {e}")
                break
    print(f"Processed {idx}/{len(urls)} URLs")

