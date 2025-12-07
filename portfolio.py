import streamlit as st
import requests

# ============================================================================
# NEW PORTFOLIO STRUCTURE (CORE TEMPLATE)
# ============================================================================
# This file provides the structure for a portfolio website with:
# - Blog/Notes system
# - AI Algorithms
# - OOP Design Patterns
# - API Fundamentals
# - Coding Principles
# - Streamlit Mini Projects
# - External links to your Streamlit note apps
#
# You will plug in your external Streamlit links as needed.
# ============================================================================

# --- PAGE CONFIG ---
st.set_page_config(page_title="Jawaad Hendricks | Portfolio", page_icon="🤖", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.title("Jawaad Hendricks")
    st.write("AI Research • Software Engineering • OOP Architecture")
    st.divider()
    st.subheader("Links")
    st.write("📘 **Main Notes App:**")
    st.link_button("OOP Notes (Streamlit)", "https://liveprojects-5yrc8eepxwuwwc8gcquhw3.streamlit.app/")
    st.write("🔗 GitHub: https://github.com/yourusername")
    st.write("💼 LinkedIn: https://linkedin.com/in/yourprofile")
    st.write("✉️ Email: your.email@example.com")

# ============================================================================
# HERO SECTION
# ============================================================================
st.markdown("""
# 👋 Welcome

I'm **Jawaad**, a Computer Science student deeply exploring:
- AI Algorithms (agents, embeddings, LLM reasoning)
- API engineering & systems integration
- Clean OOP architecture and design patterns
- Streamlit products & rapid prototyping

This site serves as a **blog-portfolio hybrid**, where I document everything through running templates, code, and live apps.
""")

st.divider()

# ============================================================================
# SECTION: Blog / Notes
# ============================================================================
st.header("📘 Blog / Notes")
st.write("Your knowledge base of everything you’ve been studying.")

notes = [
    {
        "title": "OOP Design Patterns — Factory Pattern",
        "desc": "Deep dive into creational design patterns with examples.",
        "link": "https://liveprojects-ayqlemdgahmimmr7ugodkf.streamlit.app/",
    },
    {
        "title": "API Fundamentals — REST, requests, authentication",
        "desc": "Notes on designing and consuming APIs effectively.",
        "link": "https://liveprojects-ayqlemdgahmimmr7ugodkf.streamlit.app/",
    },
    {
        "title": "Code Architecture — SOLID, abstraction, dependency inversion",
        "desc": "Full breakdown of scalable system design principles.",
        "link": "#",
        "link": "#"
    },
    {
        "title": "Streamlit Mini Projects",
        "desc": "All small experiments and UI prototypes.",
        "link": "#",
    }
]

for n in notes:
    with st.container():
        st.subheader(n["title"])
        st.write(n["desc"])
        st.link_button("Open", n["link"])
        st.markdown("---")

# ============================================================================
# SECTION: Project Categories
# ============================================================================
st.header("🧠 AI Projects")
st.write("Real implementations of agent systems, automation tools, and experiment logs.")
st.markdown("---")

st.header("🛠️ Software Engineering Projects")
st.write("Everything from OOP experiments to full-stack builds.")
st.markdown("---")

st.header("📚 50-Project Journey")
st.write("Tracking all micro projects across AI, OOP, APIs, and automation.")
st.markdown("---")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("""
<div style='text-align: center; margin-top: 40px; color: gray;'>
    © 2025 Jawaad Hendricks — Streamlit Portfolio
</div>
""", unsafe_allow_html=True)



