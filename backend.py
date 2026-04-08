import os
from pypdf import PdfReader
from docx import Document


# ---------- TEXT EXTRACTION ----------
def extract_text(file_path):
    text = ""

    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"

    return text.lower()


# ---------- COMMON LOGIC ----------
def evaluate_agent(skill_dict, resume_text, jd_text, agent_name):
    matched = []
    missing = []
    total = 0

    for skill, variations in skill_dict.items():
        if any(v in jd_text for v in variations):
            total += 1

            if any(v in resume_text for v in variations):
                matched.append(skill)
            else:
                missing.append(skill)

    score = (len(matched) / total) * 100 if total > 0 else 0

    return {
        "agent": agent_name,
        "score": round(score, 2),
        "matched": matched,
        "missing": missing
    }


# ---------- AGENTS ----------
def seo_agent(resume_text, jd_text):
    seo_skills = {
        "seo": ["seo", "search engine optimization"],
        "keyword research": ["keyword research"],
        "on page seo": ["on page seo"],
        "off page seo": ["off page seo", "backlinks"],
        "google analytics": ["google analytics"]
    }
    return evaluate_agent(seo_skills, resume_text, jd_text, "SEO")


def ads_agent(resume_text, jd_text):
    ads_skills = {
        "google ads": ["google ads"],
        "facebook ads": ["facebook ads", "meta ads"],
        "ppc": ["ppc", "pay per click"],
        "campaign management": ["campaign management"],
        "conversion tracking": ["conversion tracking"]
    }
    return evaluate_agent(ads_skills, resume_text, jd_text, "Ads")


def social_agent(resume_text, jd_text):
    social_skills = {
        "social media": ["social media", "social media marketing"],
        "content creation": ["content creation"],
        "instagram marketing": ["instagram"],
        "facebook marketing": ["facebook"],
        "linkedin marketing": ["linkedin"]
    }
    return evaluate_agent(social_skills, resume_text, jd_text, "Social Media")


# ---------- FINAL DECISION ----------
def final_decision(resume_text, jd_text):
    seo = seo_agent(resume_text, jd_text)
    ads = ads_agent(resume_text, jd_text)
    social = social_agent(resume_text, jd_text)

    final_score = (seo["score"] + ads["score"] + social["score"]) / 3

    if final_score >= 70:
        decision = "Strongly Shortlisted"
    elif final_score >= 50:
        decision = "Shortlisted"
    else:
        decision = "Rejected"

    return {
        "final_score": round(final_score, 2),
        "decision": decision,
        "agents": [seo, ads, social]
    }