import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_suggestions(resume_text, jd_text, score, missing_skills):
    missing = ', '.join(missing_skills[:6]) if missing_skills else "None"

    prompt = f"""
You are an expert resume coach helping a student get an internship.

ATS Score: {score}/100
Missing Skills: {missing}

Resume (first 1500 chars):
{resume_text[:1500]}

Job Description (first 800 chars):
{jd_text[:800]}

Give exactly:
1. 5 specific bullet points to improve this resume for this job
2. 2 rewritten resume bullet points that are stronger with metrics
3. 1 short tip about the missing skills

Be specific, concise, and actionable. Use simple language.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800
    )
    return response.choices[0].message.content