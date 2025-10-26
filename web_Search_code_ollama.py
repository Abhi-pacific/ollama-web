# import ollama
# import os

# os.environ["OLLAMA_API_KEY"] = "4d169e51df3c4acd9ceffc25a9798ecc.SzxaICfxVVvaMFg1iaUBuwUF"
# response = ollama.web_fetch('https://www.5dariyanews.com/news/468590-Axis-Bank-opens-branch-at-Doda')
# print(response)
# print('done')
# Install requirements first (inside your venv):
# pip install ollama pydantic

from ollama import chat, web_fetch
from pydantic import BaseModel
import json

# Step 1: Fetch article text using Ollama web_fetch
article = web_fetch("https://www.cnbctv18.com/personal-finance/axis-bank-launches-india-first-gold-backed-credit-on-upi-19695598.htm")

# Step 2: Define the structured schema using Pydantic
class ArticleInfo(BaseModel):
    title: str
    author: str | None = None
    publish_date: str | None = None

# Step 3: Craft a prompt for structured extraction
prompt = f"""
Below is the content of a news article. 
Extract the following fields in JSON format that fits this schema:
title, author, publish_date, source_url, summary.

Return ONLY valid JSON that matches the schema.

CONTENT:
{article.content}
"""

# Step 4: Call the Ollama model with structured JSON schema
response = chat(
    model="llama3.2:latest",                     # You can replace with any suitable model
    messages=[{"role": "user", "content": prompt}],
    format=ArticleInfo.model_json_schema()  # Forces JSON structure
)

# Step 5: Validate and print result using Pydantic
article_info = ArticleInfo.model_validate_json(response.message.content)

# Pretty print as formatted JSON
print(json.dumps(article_info.model_dump(), indent=2, ensure_ascii=False))


