import streamlit as st
import pandas as pd
import numpy as np 
import plotly.graph_objects as go
import random
from math import ceil
import datetime

st.set_page_config(page_title="Ultimate Math Tutor", layout="wide")

# -------------------------
# GLOBAL DATA STRUCTURES
# -------------------------
RULES_DATA = [
    {"id": "PARA", "name": "Parabola", "formula": r"y = ax^2 + q", "desc": "Turning point: (0, q). 'a' > 0 is a smile, 'a' < 0 is a frown."},
    {"id": "HYP", "name": "Hyperbola", "formula": r"y = \frac{a}{x} + q", "desc": "Asymptotes at x=0 and y=q. 'a' moves curves between quadrants."},
    {"id": "EXP", "name": "Exponential", "formula": r"y = a \cdot b^x + q", "desc": "Horizontal asymptote at y=q. 'b' > 1 is growth, 0 < b < 1 is decay."},
    {"id": "TRIG", "name": "Sine Wave", "formula": r"y = a\sin(x) + q", "desc": "Periodic wave. 'a' is amplitude, 'q' is rest position."},
]

# -------------------------
# RENDERERS
# -------------------------
def render_theory_overview():
    st.header("📚 The Function Gallery")
    st.write("Master these shapes to ace Grade 11 Graph Interpretation.")
    
    cols = st.columns(2)
    for i, r in enumerate(RULES_DATA):
        with cols[i % 2]:
            with st.container(border=True):
                st.subheader(r["name"])
                st.latex(r["formula"])
                st.write(r["desc"])

def render_visualization_lab():
    st.header("🎮 Multiverse Graph Lab")
    st.markdown("Experiment with **Stretch (a)** and **Shift (q)**.")

    c1, c2 = st.columns([1, 2])
    with c1:
        func_choice = st.selectbox("Select Function Type", ["Parabola", "Hyperbola", "Exponential", "Sine"])
        a = st.slider("Stretch/Amplitude (a)", -5.0, 5.0, 1.0, 0.5)
        q = st.slider("Vertical Shift (q)", -5.0, 5.0, 0.0, 0.5)
        
        if func_choice == "Exponential":
            b = st.radio("Base (b)", [2.0, 0.5], horizontal=True)
        else:
            b = 1.0

    with c2:
        fig = go.Figure()
        
        if func_choice == "Parabola":
            x = np.linspace(-10, 10, 400)
            y = a * (x**2) + q
            
        elif func_choice == "Hyperbola":
            x1 = np.linspace(-10, -0.1, 200)
            x2 = np.linspace(0.1, 10, 200)
            y1 = (a / x1) + q
            y2 = (a / x2) + q
            fig.add_trace(go.Scatter(x=x1, y=y1, name="Branch 1", line=dict(color='blue', width=3)))
            fig.add_trace(go.Scatter(x=x2, y=y2, name="Branch 2", line=dict(color='blue', width=3)))
            x = np.concatenate([x1, x2]); y = np.concatenate([y1, y2])
            
        elif func_choice == "Exponential":
            x = np.linspace(-5, 5, 400)
            y = a * (b**x) + q
            

[Image of an exponential growth and decay graph]

        else: # Sine
            x = np.linspace(0, 360, 500)
            y = a * np.sin(np.radians(x)) + q
            

        if func_choice != "Hyperbola":
            fig.add_trace(go.Scatter(x=x, y=y, name="Result", line=dict(color='blue', width=3)))

        # Add Asymptote Line
        fig.add_hline(y=q, line_dash="dash", line_color="red", annotation_text=f"y = {q}")
        
        fig.update_layout(yaxis=dict(range=[-10, 10]), template="plotly_white", height=500)
        st.plotly_chart(fig, use_container_width=True)

def render_test_page():
    st.header("📝 Graded Assessment")
    
    if st.session_state.show_grade_result:
        st.success(f"Graded! Your score: {st.session_state.last_score}")
    
    with st.form("test_form"):
        st.write("Q1: If $y = 3x^2 + 2$, what is the turning point?")
        ans1 = st.text_input("Answer Q1", placeholder="(x, y)")
        
        st.write("Q2: In $y = \\frac{2}{x} - 4$, what is the horizontal asymptote?")
        ans2 = st.text_input("Answer Q2", placeholder="y = ...")
        
        if st.form_submit_button("Submit Answers"):
            # Simple grading logic for demo
            correct = 0
            if "0,2" in ans1.replace(" ", ""): correct += 1
            if "-4" in ans2: correct += 1
            
            score_str = f"{correct}/2"
            st.session_state.test_submissions.append({
                "Time": datetime.datetime.now().strftime("%H:%M"),
                "Score": score_str,
                "Percent": (correct/2)*100
            })
            st.session_state.last_score = score_str
            st.session_state.show_grade_result = True
            st.rerun()

def render_analytics():
    st.header("📊 Progress Tracker")
    if st.session_state.test_submissions:
        df = pd.DataFrame(st.session_state.test_submissions)
        st.line_chart(df, x="Time", y="Percent")
        st.table(df)
    else:
        st.info("Complete a test to see results.")

# -------------------------
# MAIN APP FLOW
# -------------------------
def main():
    # 1. Initialize State
    if 'test_submissions' not in st.session_state:
        st.session_state.test_submissions = []
    if 'show_grade_result' not in st.session_state:
        st.session_state.show_grade_result = False
    if 'last_score' not in st.session_state:
        st.session_state.last_score = ""

    # 2. Sidebar Navigation
    st.sidebar.title("Math Tutor Tool")
    menu = ["Theory Gallery", "Live Graph Lab", "Assessment", "Analytics"]
    choice = st.sidebar.radio("Navigation", menu)

    # 3. Page Routing
    if choice == "Theory Gallery":
        render_theory_overview()
    elif choice == "Live Graph Lab":
        render_visualization_lab()
    elif choice == "Assessment":
        render_test_page()
    elif choice == "Analytics":
        render_analytics()

if __name__ == "__main__":
    main()
