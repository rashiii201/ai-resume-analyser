import json
import re
import subprocess
imoprt sys

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    import spacy
    nlp = spacy.load("en_core_web_sm")

from keybert import KeyBERT
from rapidfuzz import fuzz

kw_model = KeyBERT()

# Load skills database
with open("data/skills.json", "r") as f:
    SKILLS_DB = json.load(f)

ALL_SKILLS = SKILLS_DB["technical_skills"] + SKILLS_DB["soft_skills"]

def extract_contact_info(text):
    email = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phone = re.findall(r'[\+\(]?[1-9][0-9\s\-\(\)]{7,14}[0-9]', text)
    linkedin = re.findall(r'linkedin\.com/in/[\w\-]+', text, re.IGNORECASE)
    github = re.findall(r'github\.com/[\w\-]+', text, re.IGNORECASE)
    return {
        "email": email[0] if email else None,
        "phone": phone[0] if phone else None,
        "linkedin": linkedin[0] if linkedin else None,
        "github": github[0] if github else None
    }

def extract_name(text):
    doc = nlp(text[:300])  # name is usually at the top
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    # fallback: first line
    return text.split('\n')[0].strip().split('|')[0].strip()

def extract_skills(text):
    found_skills = []
    text_lower = text.lower()
    for skill in ALL_SKILLS:
        if len(skill) <= 2:  
            continue
        if fuzz.partial_ratio(skill.lower(), text_lower) >= 90:
            found_skills.append(skill)
    return list(set(found_skills))

def extract_sections(text):
    sections = {}
    section_headers = {
        "summary": r'(professional summary|summary|objective|profile)',
        "experience": r'(experience|work experience|employment)',
        "education": r'(education|academic|qualification)',
        "skills": r'(skills|technical skills|core competencies)',
        "projects": r'(projects|personal projects|key projects)',
        "certifications": r'(certifications|certificates|courses)'
    }
    text_lower = text.lower()
    for section, pattern in section_headers.items():
        match = re.search(pattern, text_lower)
        sections[section] = "present" if match else "missing"
    return sections

def extract_all(text):
    return {
        "name": extract_name(text),
        "contact": extract_contact_info(text),
        "skills": extract_skills(text),
        "sections": extract_sections(text)
    }