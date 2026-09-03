#  AI Resume Analyser

> An end-to-end NLP-powered web application that analyses resumes against job descriptions, generates ATS scores, detects skill gaps, and provides AI-driven improvement suggestions.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56-red?style=flat&logo=streamlit)
![spaCy](https://img.shields.io/badge/spaCy-3.8-09A3D5?style=flat&logo=spacy)
![Sentence BERT](https://img.shields.io/badge/Sentence--BERT-all--MiniLM--L6--v2-orange?style=flat)
![Groq](https://img.shields.io/badge/Groq-LLaMA3--70B-green?style=flat)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)

---

##  Live Demo

 **[Try it here → ai-resume-analyser.streamlit.app](https://ai-resume-analyser-4p9b6vipblcpdwrkctt5wk.streamlit.app/)**

---

##  What It Does

Upload any resume (PDF/DOCX) and paste a job description — the app will:

- **Parse** the resume and extract structured information
- **Extract** skills, contact info, name, and section completeness using NLP
- **Match** the resume against the job description using Sentence-BERT embeddings
- **Score** the resume with a weighted ATS scoring system
- **Identify** matched and missing skills with fuzzy matching
- **Generate** personalized AI suggestions using LLaMA 3 via Groq API

---

##  Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| PDF Parsing | pdfplumber, PyMuPDF |
| NLP Extraction | spaCy (NER), KeyBERT, rapidfuzz |
| Semantic Matching | Sentence-BERT (`all-MiniLM-L6-v2`) |
| Skill Gap Detection | Cosine Similarity + Fuzzy Matching |
| ATS Scoring | Custom weighted formula |
| AI Suggestions | LLaMA 3.3-70B via Groq API |
| Deployment | Streamlit Cloud |

---

##  Project Architecture

```
ai-resume-analyser/
├── app.py                  # Streamlit frontend
├── backend/
│   ├── parser.py           # PDF/DOCX text extraction
│   ├── extractor.py        # NLP: NER, skills, sections
│   ├── matcher.py          # Sentence-BERT semantic matching
│   ├── scorer.py           # Weighted ATS score calculator
│   └── suggester.py        # Groq LLM suggestion engine
├── data/
│   └── skills.json         # Skills database (technical + soft)
├── requirements.txt
└── .gitignore
```

---

##  How It Works

### 1. Resume Parsing
Dual-engine PDF extraction using `pdfplumber` (primary) and `PyMuPDF` (fallback) ensures accurate text extraction from any resume format.

### 2. NLP Information Extraction
- **Named Entity Recognition** via spaCy to extract name, organizations, dates
- **Keyword extraction** via KeyBERT for top skills
- **Fuzzy matching** via rapidfuzz against a 60+ skills database
- **Section detection** using regex pattern matching

### 3. JD Matching Engine
Resume and job description are encoded using **Sentence-BERT** (`all-MiniLM-L6-v2`) and compared via **cosine similarity** — capturing semantic meaning beyond simple keyword overlap.

### 4. ATS Scoring Formula

| Component | Weight |
|---|---|
| Semantic Match (SBERT) | 40% |
| Skill Match % | 35% |
| Section Completeness | 25% |

### 5. AI Suggestions
The resume, JD, score, and missing skills are sent to **LLaMA 3.3-70B** (via Groq API) which returns:
- 5 specific improvement bullet points
- 2 rewritten resume bullets with metrics
- 1 actionable tip for missing skills

---

##  Run Locally

### Prerequisites
- Python 3.10+
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Setup

```bash
# Clone the repo
git clone https://github.com/rashiii201/ai-resume-analyser.git
cd ai-resume-analyser

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo GROQ_API_KEY=your_key_here > .env

# Run the app
streamlit run app.py
```

---

##  Sample Results

| Metric | Score |
|---|---|
| Semantic Match | 73.3 / 100 |
| Skill Match | 77.8% |
| Section Completeness | 100% |
| **Final ATS Score** | **81.5 / 100 — Excellent** |

---

##  Key Features

-  Works with both PDF and DOCX resumes
-  Dual-engine PDF parsing for maximum compatibility
-  Semantic understanding — not just keyword matching
-  Real skill gap detection with fuzzy matching
-  AI-generated, role-specific suggestions
-  Clean, interactive Streamlit UI
-  Free to use and deploy

---

##  Skills Demonstrated

`Natural Language Processing` · `Named Entity Recognition` · `Transformer Models` · `Sentence Embeddings` · `Cosine Similarity` · `Fuzzy String Matching` · `Prompt Engineering` · `Streamlit` · `PDF Parsing` · `Git & GitHub` 

---

##  Dataset

Skills database (`data/skills.json`) contains 60+ curated technical and soft skills across domains including Machine Learning, Cloud, Web Development, Data Science, and DevOps.

---

## Author

**Rashi Sharma**
- GitHub: [@rashiii201](https://github.com/rashiii201)
- Email: rashisrma101@gmail.com
- LinkedIn: [linkedin.com/in/rashi-sharma](https://linkedin.com/in/rashi-sharma)

