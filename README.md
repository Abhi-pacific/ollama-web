# 🔬 Ollama Web Search & Author Extraction

Extract structured article metadata (title, author, confidence score) from news URLs using **Ollama's web_fetch + LLM chat** — fully local, zero external API calls.

## 📋 Problem Statement

When processing media mentions or building news databases, article author information is often:
- Unstructured or embedded in complex HTML
- Missing from obvious metadata fields
- Difficult to extract reliably with regex

This tool uses a **local LLM** (via Ollama) to intelligently extract article metadata from URLs with structured, validated output.

## 🔧 Approach

### Pipeline Overview

1. **Load URLs** from an Excel file (filtered by media resource type)
2. **Fetch article content** using `ollama.web_fetch()` — retrieves article text and HTML
3. **Extract metadata** via `ollama.chat()` with a structured prompt:
   - `title` — article title
   - `author` — author name or publishing organization
   - `confidence` — 0-100 score indicating extraction reliability
4. **Validate output** with Pydantic models for structured, consistent results
5. **Batch process** all URLs and collect results

### Author Extraction Logic

The prompt uses a **priority-based extraction strategy**:

1. **Priority 1:** HTML meta tags (`author`, `byline`, `publisher`) and structured data (JSON-LD)
2. **Priority 2:** Article body scanning for attribution phrases ("press release provided by", "published by", "source:")
3. **Priority 3:** Organizational/brand sources (e.g., "VMPL" in press releases)
4. **Exclusions:** Quoted individuals, experts mentioned, interviewees — these are content subjects, not authors

### Confidence Scoring

| Score Range | Meaning |
|-------------|---------|
| 90-100% | Author found in reliable metadata (meta tags, structured data) |
| 70-89% | Clear organizational attribution in article body |
| 50-69% | Indirect references or partial attribution |
| 1-49% | Weak or inferred attribution |
| 0% | No author information found |

## 📊 Example Output

```json
{
  "title": "India's Renewable Energy Capacity Crosses 200 GW Milestone",
  "author": "Press Trust of India",
  "confidence": 94
}
```

## 📁 Project Structure

```
ollama-web/
├── web_Search_code_ollama.py    # Main pipeline script
├── testingcode.py               # Testing/exploration code
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3 | Core language |
| Ollama | Local LLM inference (`web_fetch` + `chat`) |
| Pydantic | Structured data validation (BaseModel schemas) |
| Pandas | Excel data loading and batch processing |

## 🚀 How to Run

```bash
# Clone
git clone https://github.com/Abhi-pacific/ollama-web.git
cd ollama-web

# Install dependencies
pip install -r requirements.txt

# Make sure Ollama is running locally with a model loaded
# ollama serve
# ollama pull mistral

# Update the Excel file path in the script to point to your data
# Run the pipeline
python web_Search_code_ollama.py
```

## 💡 Key Features

- ✅ **Fully local** — Ollama runs on your machine, no external API costs
- ✅ **Structured output** — Pydantic-validated JSON with consistent schema
- ✅ **Confidence scoring** — Each extraction rated 0-100 for reliability
- ✅ **Smart author detection** — Distinguishes real authors from mentioned individuals
- ✅ **Batch processing** — Reads URLs from Excel for scalable processing

## 👨‍💻 Author

**Abhishek Chauhan** — Data Analyst @ Netimpact Solutions  
[LinkedIn](https://linkedin.com/in/abhishek-chauhan-28c) | [Email](mailto:Chauhan.a.abhishek@icloud.com)

---

*Part of my AI/ML portfolio. Check out my other projects on [GitHub](https://github.com/Abhi-pacific).*
