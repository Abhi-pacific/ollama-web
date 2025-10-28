import requests
html_response = requests.get("https://www.britishcolumbiatimes.com/news/axis-max-life-india-consumption-opportunities-fund-taps-consumption-growth20251016174739/")
html_text = html_response.content
print(html_text)

