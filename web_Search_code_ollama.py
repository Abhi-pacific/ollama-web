# import ollama
import os

os.environ["OLLAMA_API_KEY"] = "4d169e51df3c4acd9ceffc25a9798ecc.SzxaICfxVVvaMFg1iaUBuwUF"
# response = ollama.web_fetch('https://www.5dariyanews.com/news/468590-Axis-Bank-opens-branch-at-Doda')
# print(response)
# print('done')
# Install requirements first (inside your venv):
# pip install ollama pydantic

from ollama import chat, web_fetch
from pydantic import BaseModel
import json

#list of the URLS
urls = [
   "https://www.bizzbuzz.news/markets/stock-market/bulls-take-charge-on-dalal-street-on-fresh-fii-inflows-1374928"
]




for i in urls:
    # Step 1: Fetch article text using Ollama web_fetch
    article = web_fetch(i)

    # Step 2: Define the structured schema using Pydantic
    class ArticleInfo(BaseModel):
        title: str
        author: str | None = None
        confidence: int  # confidence percentage from 0 to 100

    # Step 3: Craft a prompt for structured extraction
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

    # Step 4: Call the Ollama model with structured JSON schema
    response = chat(
        model="deepseek-r1:1.5b",                     # You can replace with any suitable model
        messages=[{"role": "user", "content": prompt}],
        format=ArticleInfo.model_json_schema()  # Forces JSON structure
    )

    # Step 5: Validate and print result using Pydantic
    article_info = ArticleInfo.model_validate_json(response.message.content)

    # Pretty print as formatted JSON
    print(json.dumps(article_info.model_dump(), indent=2, ensure_ascii=False))


