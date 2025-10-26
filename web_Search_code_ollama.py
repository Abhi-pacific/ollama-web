import ollama
import os

os.environ["OLLAMA_API_KEY"] = "4d169e51df3c4acd9ceffc25a9798ecc.SzxaICfxVVvaMFg1iaUBuwUF"
response = ollama.web_fetch('https://www.5dariyanews.com/news/468590-Axis-Bank-opens-branch-at-Doda')
print(response)
print('done')