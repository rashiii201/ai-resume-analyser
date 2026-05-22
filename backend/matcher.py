from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import fuzz

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_semantic_score(resume_text, jd_text):
    embeddings = model.encode([resume_text, jd_text])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return round(float(score) * 100, 2)

def get_skill_gap(resume_skills, jd_skills):
    missing = []
    matched = []
    for jd_skill in jd_skills:
        found = False
        for r_skill in resume_skills:
            if fuzz.ratio(jd_skill.lower(), r_skill.lower()) >= 80:
                matched.append(jd_skill)
                found = True
                break
        if not found:
            missing.append(jd_skill)
    return {
        "matched": matched,
        "missing": missing,
        "match_percent": round(len(matched) / max(len(jd_skills), 1) * 100, 1)
    }

def match(resume_text, jd_text, resume_skills, jd_skills):
    semantic_score = get_semantic_score(resume_text, jd_text)
    skill_gap = get_skill_gap(resume_skills, jd_skills)
    return {
        "semantic_score": semantic_score,
        "skill_match": skill_gap
    }