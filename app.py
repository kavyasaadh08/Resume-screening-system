import streamlit as st
import os
from backend import extract_text, final_decision


st.set_page_config(page_title="Resume Screener", layout="wide")

st.title("Resume Screening System")

# Upload resumes
uploaded_files = st.file_uploader(
    "Upload resumes (PDF or DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

# Job description input
jd_text = st.text_area("Paste Job Description")


# ---------- MAIN BUTTON ----------
if st.button("Screen Resumes"):

    if not uploaded_files:
        st.warning("Please upload resumes")
    elif not jd_text:
        st.warning("Please paste Job Description")
    else:
        results = []

        for file in uploaded_files:
            temp_path = f"temp_{file.name}"

            with open(temp_path, "wb") as f:
                f.write(file.getbuffer())

            resume_text = extract_text(temp_path)
            result = final_decision(resume_text, jd_text.lower())

            results.append({
                "name": file.name,
                "score": result["final_score"],
                "decision": result["decision"],
                "details": result
            })

        # Sort by best score
        results = sorted(results, key=lambda x: x["score"], reverse=True)

        # Split
        shortlisted = [r for r in results if "Shortlisted" in r["decision"]]
        rejected = [r for r in results if "Rejected" in r["decision"]]

        st.divider()

        # ---------- SHORTLISTED ----------
        st.subheader("✅ Shortlisted Candidates")

        if shortlisted:
            for r in shortlisted:
                st.write(f"**{r['name']} → {r['score']}%**")

                with st.expander("View Details"):
                    for agent in r["details"]["agents"]:
                        st.write(f"**{agent['agent']}**")
                        st.write(f"Matched Skills: {agent['matched']}")

                    st.success("Fits well for digital marketing role due to relevant skills.")
        else:
            st.write("No shortlisted candidates")

        # ---------- REJECTED ----------
        st.subheader("❌ Rejected Candidates")

        if rejected:
            for r in rejected:
                st.write(f"**{r['name']} → {r['score']}%**")

                with st.expander("View Details"):
                    for agent in r["details"]["agents"]:
                        st.write(f"**{agent['agent']}**")
                        st.write(f"Missing Skills: {agent['missing']}")

                    st.error("Missing key skills required for this role.")
        else:
            st.write("No rejected candidates")