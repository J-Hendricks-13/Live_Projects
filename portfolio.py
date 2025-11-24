import streamlit as st

# --- CONFIGURATION & CONTENT ---

# Page Settings
PAGE_TITLE = "Firstname Lastname | Developer Portfolio"
PAGE_ICON = "💻"
PROFILE_PICTURE = "https://placehold.co/150x150/3B82F6/FFFFFF?text=FNL" # Placeholder URL - Replace with your own image URL!

# Contact/Sidebar Info
EMAIL = "your.email@example.com"
LINKEDIN = "https://linkedin.com/in/yourprofile"
GITHUB = "https://github.com/yourusername"
CV_URL = "#" # Replace with a link to your CV PDF

# --- Content Data Structures ---

ABOUT_ME = """
Hi, I'm **Firstname Lastname**! 

I am a final-year Computer Science student with a strong focus on building scalable applications and leveraging data for insight. My core strengths lie in Python (including frameworks like Streamlit and Django), JavaScript, and cloud technologies (AWS/Azure). I thrive in environments that challenge me to integrate complex systems and deliver user-centric solutions.

I am actively seeking full-time Software Engineer or Data Scientist roles starting in 2024/2025.
"""

EDUCATION = {
    "University Name": "BSc (Hons) Computer Science",
    "Dates": "2021 - 2025 (Expected)",
    "GPA": "First Class Honours (Current Average: 78%)",
    "Highlights": [
        "Focused on advanced algorithms, distributed systems, and modern software design.",
        "Completed a major dissertation project on Machine Learning for time-series forecasting.",
    ]
}

MODULES = [
    {"icon": "⚙️", "title": "Advanced Algorithms", "desc": "Study of complexity, graph theory, and dynamic programming."},
    {"icon": "📊", "title": "Database Systems", "desc": "SQL, NoSQL (MongoDB), database design, and optimization."},
    {"icon": "🤖", "title": "Machine Learning", "desc": "Implemented models (clustering, classification) using Scikit-learn and TensorFlow."},
    {"icon": "🌐", "title": "Web Development (Full Stack)", "desc": "Experience with React, Flask/Django, and REST API creation."},
    {"icon": "☁️", "title": "Cloud Computing (AWS)", "desc": "Fundamentals of EC2, S3, Lambda, and serverless architectures."},
]

PROJECTS = [
    {
        "title": "Real-time Stock Ticker Dashboard (Streamlit)",
        "desc": "A data visualization application displaying historical and live stock prices using Yahoo Finance API and Pandas.",
        "link": "https://live-project-link-1.streamlit.app/", # Replace with live link
        "tech": "Python, Streamlit, Pandas, API"
    },
    {
        "title": "E-commerce API Backend (Django)",
        "desc": "Developed a robust RESTful API for an e-commerce platform, handling user authentication, product management, and order processing.",
        "link": "https://github.com/yourusername/django-ecommerce", # Replace with GitHub link
        "tech": "Python, Django, Django Rest Framework, PostgreSQL"
    },
    {
        "title": "Collaborative Whiteboard App (React & Firebase)",
        "desc": "A real-time whiteboard allowing multiple users to draw and collaborate simultaneously. Utilized Firestore for state sync.",
        "link": "https://live-project-link-3.web.app/", # Replace with live link
        "tech": "React, JavaScript, Firestore, HTML/CSS"
    },
]

# --- STREAMLIT APP LAYOUT ---

# Set the page configuration
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

# Custom CSS for aesthetics
st.markdown(
    """
    <style>
    /* Global Background and Text Color */
    .stApp {
        background-color: #0d1117; /* Dark background similar to GitHub */
        color: #c9d1d9;
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        color: #58a6ff; /* Accent blue for titles */
    }
    
    /* Section Divider/Title Style */
    .section-header {
        border-bottom: 2px solid #58a6ff;
        padding-bottom: 10px;
        margin-top: 30px;
        margin-bottom: 20px;
    }

    /* Card Styling for Modules and Projects */
    .st-emotion-cache-1pxi9b9 { /* Target container for st.container */
        background-color: #161b22;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #30363d;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    </style>
    """, 
    unsafe_allow_html=True
)


# --- SIDEBAR (Contact Info) ---
with st.sidebar:
    st.image(PROFILE_PICTURE, width=120)
    st.header("Contact")
    st.markdown(f"**Email:** [{EMAIL}](mailto:{EMAIL})")
    st.markdown(f"**LinkedIn:** [Profile]({LINKEDIN})")
    st.markdown(f"**GitHub:** [Repo]({GITHUB})")
    st.divider()
    st.download_button(
        label="Download CV",
        data="Placeholder CV Content", # Replace with actual file upload or link handling if needed
        file_name="Firstname_Lastname_CV.pdf",
        mime="application/pdf",
        help="Click to download my detailed curriculum vitae.",
        key='cv_download_btn'
    )


# --- MAIN CONTENT ---

# 1. Title & Bio Section
st.header("Welcome to my Developer Portfolio", divider='blue')
st.title(f"I'm {EDUCATION['University Name'].split()[0]} Student")

st.markdown(ABOUT_ME)

st.write("---") # Simple divider

# 2. Qualifications & Education
st.markdown('<h2 class="section-header">Education & Qualifications</h2>', unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader(EDUCATION["University Name"])
        st.write(f"*{EDUCATION['Dates']}*")
        st.markdown(f"**{EDUCATION['GPA']}**")
    
    with col2:
        st.markdown(f"### {EDUCATION['University Name']}")
        st.markdown("---")
        for highlight in EDUCATION["Highlights"]:
            st.markdown(f"- {highlight}")


st.write("#") # Vertical space

# 3. University Modules
st.markdown('<h2 class="section-header">Key University Modules</h2>', unsafe_allow_html=True)

# Use columns for a responsive grid of modules
cols = st.columns(3)
for i, module in enumerate(MODULES):
    with cols[i % 3]: # Cycle through 3 columns
        with st.container():
            st.markdown(f"**{module['icon']} {module['title']}**")
            st.caption(module["desc"])
            st.markdown("---")


st.write("#") # Vertical space

# 4. Projects Section
st.markdown('<h2 class="section-header">Live Projects & Portfolio Work</h2>', unsafe_allow_html=True)

for project in PROJECTS:
    st.container()
    col_l, col_r = st.columns([3, 1])
    
    with col_l:
        st.subheader(project["title"])
        st.write(project["desc"])
        st.caption(f"**Tech Stack:** {project['tech']}")
    
    with col_r:
        st.markdown("#") # Add vertical space for alignment
        st.link_button("View Live Project / GitHub", project["link"], type="primary")

    st.markdown("---")


# Footer
st.markdown(
    """
    <br>
    <div style='text-align: center; color: #6e7681;'>
        Built with Python and Streamlit | Last Updated: 2024
    </div>
    """,
    unsafe_allow_html=True
)