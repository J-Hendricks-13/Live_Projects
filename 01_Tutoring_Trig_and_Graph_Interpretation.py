import streamlit as st
import pandas as pd
import numpy as np 
import plotly.graph_objects as go
import random
from math import ceil
import datetime

st.set_page_config(page_title="Ultimate Function Explorer", layout="wide")

# -------------------------
# DATA: ALGEBRAIC FUNCTIONS
# -------------------------
RULES_DATA = [
    {"id": "PARA_01", "name": "Parabola (Quadratic)", "formula": r"y = ax^2 + q", "description": "A U-shaped curve. 'a' determines width/direction, 'q' is the turning point shift."},
    {"id": "HYP_01", "name": "Hyperbola", "formula": r"y = \frac{a}{x} + q", "description": "Two curves with asymptotes. 'x=0' is the vertical asymptote; 'y=q' is the horizontal asymptote."},
    {"id": "EXP_01", "name": "Exponential", "formula": r"y = a \cdot b^x + q", "description": "A curve that grows or decays. It never touches the horizontal asymptote at 'y=q'."},
    {"id": "TRIG_01", "name": "Trig (Sine)", "formula": r"y = a\sin(x) + q", "description": "A periodic wave. 'a' is amplitude, 'q' is the rest position."},
]

# -------------------------
# RENDERER: LIVE GRAPH LAB (ALGEBRAIC + TRIG)
# -------------------------
def render_visualization_tab():
    st.header("🎮 Multiverse Graph Lab")
    st.markdown("Select a function type to explore its unique shape and how $a$ and $q$ transform it.")

    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Function Settings")
        func_choice = st.selectbox("Select Function Type", ["Parabola", "Hyperbola", "Exponential", "Sine"])
        
        # Dynamic Sliders based on function
        a = st.slider("Stretch Factor (a)", -5.0, 5.0, 1.0, 0.5)
        q = st.slider("Vertical Shift (q)", -5.0, 5.0, 0.0, 0.5)
        
        if func_choice == "Exponential":
            b = st.selectbox("Base value (b)", [2, 3, 0.5], help="Determines growth (b>1) or decay (0<b<1)")
        
    with c2:
        # Generate Data based on choice
        fig = go.Figure()
        
        if func_choice == "Parabola":
            x = np.linspace(-10, 10, 400)
            y = a * (x**2) + q
            eq = f"y = {a}x^2 + {q}"
            
            
        elif func_choice == "Hyperbola":
            # Split x to avoid division by zero at x=0
            x1 = np.linspace(-10, -0.1, 200)
            x2 = np.linspace(0.1, 10, 200)
            y1 = (a / x1) + q
            y2 = (a / x2) + q
            fig.add_trace(go.Scatter(x=x1, y=y1, name="Left Branch", line=dict(color='blue', width=3)))
            fig.add_trace(go.Scatter(x=x2, y=y2, name="Right Branch", line=dict(color='blue', width=3)))
            x = np.concatenate([x1, x2])
            eq = f"y = \\frac{{{a}}}{{x}} + {q}"
            
            
        elif func_choice == "Exponential":
            x = np.linspace(-5, 5, 400)
            y = a * (b**x) + q
            eq = f"y = {a}({b})^x + {q}"
            

[Image of an exponential growth and decay graph]

            
        elif func_choice == "Sine":
            x = np.linspace(0, 360, 500)
            y = a * np.sin(np.radians(x)) + q
            eq = f"y = {a}\\sin(x) + {q}"
            

        # Add trace for non-hyperbola functions
        if func_choice != "Hyperbola":
            fig.add_trace(go.Scatter(x=x, y=y, name=func_choice, line=dict(color='blue', width=3)))

        # Add Asymptote/Reference Line
        fig.add_hline(y=q, line_dash="dash", line_color="red", annotation_text=f"Asymptote/Shift (q={q})")
        
        fig.update_layout(
            title=f"Exploring: ${eq}$",
            xaxis_title="x", yaxis_title="y",
            yaxis=dict(range=[-10, 10]),
            template="plotly_white",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

# -------------------------
# RENDERER: THEORY OVERVIEW
# -------------------------
def render_rules_overview():
    st.header("📚 The Function Gallery")
    st.write("In Grade 11, you need to recognize these four shapes instantly.")
    
    cols = st.columns(2)
    for i, r in enumerate(RULES_DATA):
        with cols[i % 2]:
            with st.container(border=True):
                st.subheader(r["name"])
                st.latex(r["formula"])
                st.write(r["description"])

# -------------------------
# MAIN LOGIC (Updated)
# -------------------------
LESSON_PAGES = {
    "1. Function Gallery": {"type": "theory_summary"},
    "2. Live Graph Lab": {"type": "visualization_tab"},
    "3. Practice (Interpreting)": {"type": "practice_interactive"},
    "4. Graded Test": {"type": "test_static"},
    "5. Analytics": {"type": "analytics_page"},
}

def main():
    # Global state init
    if 'test_submissions' not in st.session_state: st.session_state.test_submissions = []
    if 'show_grade_result' not in st.session_state: st.session_state.show_grade_result = False
    if 'last_submission_score' not in st.session_state: st.session_state.last_submission_score = ""
    if 'current_test_set_index' not in st.session_state: st.session_state.current_test_set_index = 0

    st.sidebar.title("Navigation")
    sel = st.sidebar.radio("Go to:", list(LESSON_PAGES.keys()))
    
    page_type = LESSON_PAGES[sel]["type"]
    
    if page_type == "theory_summary": render_rules_overview()
    elif page_type == "visualization_tab": render_visualization_tab()
    elif page_type == "practice_interactive": render_practice_interactive()
    elif page_type == "test_static": render_test_static()
    elif page_type == "analytics_page": render_analytics_page()

if __name__ == "__main__":
    main()    },
]

RULE_EXAMPLE_SETS = {
    "TRIG_01": [
        [(r"y = 2\sin(x)", r"a = 2"), (r"y = 0.5\cos(x)", r"a = 0.5")],
    ],
    "TRIG_02": [
        [(r"y = \sin(x) + 3", r"q = 3 \text{ (Up)}"), (r"y = \cos(x) - 2", r"q = -2 \text{ (Down)}")],
    ]
}

INTERACTIVE_PROBLEM_SETS = [
    {
        "title": "Finding a and q from a Graph",
        "problem_latex": r"\text{A graph has a maximum at } y=4 \text{ and a minimum at } y=-2. \text{ Find } a \text{ and } q.",
        "skeleton": [
            {"step_latex": r"a = \frac{4 - (-2)}{2} = 3", "correct_rule": "TRIG_01"},
            {"step_latex": r"q = \frac{4 + (-2)}{2} = 1", "correct_rule": "TRIG_02"},
            {"step_latex": r"\text{Equation: } y = 3\sin(x) + 1", "correct_rule": None},
        ],
    },
]

ALL_TEST_SETS = [
    {
        "questions": [
            {"question": r"\text{Find amplitude of } y = -4\cos(x)", "solution_steps": [r"a = |-4| = 4"], "answer": "4"},
            {"question": r"\text{Find } q \text{ for } y = \sin(x) - 5", "solution_steps": [r"q = -5"], "answer": "-5"},
        ],
        "answers": ["4", "-5"],
    }
]

LESSON_PAGES = {
    "1. Trig Fundamentals": {"type": "theory_summary"},
    "2. Amplitude (Examples)": {"type": "rule_examples", "rule_id": "TRIG_01"},
    "3. Vertical Shifts (Examples)": {"type": "rule_examples", "rule_id": "TRIG_02"},
    "4. Interpreting Graphs": {"type": "practice_interactive"},
    "5. Trig Test": {"type": "test_static"},
    "6. Progress Analytics": {"type": "analytics_page"},
    "7. Live Graph Lab": {"type": "visualization_tab"},
}

# -------------------------
# HELPERS
# -------------------------
def rotate_test_set():
    st.session_state.current_test_set_index = (st.session_state.current_test_set_index + 1) % len(ALL_TEST_SETS)
    st.session_state.show_grade_result = False

def normalize_answer(ans):
    return str(ans).replace(' ', '').lower().strip()

# -------------------------
# RENDERERS
# -------------------------
def render_rules_overview():
    st.header("📈 Trig Graph Fundamentals")
    
    for r in RULES_DATA:
        with st.container(border=True):
            st.subheader(r["name"])
            st.latex(r["formula"])
            st.write(r["description"])

def render_visualization_tab():
    st.header("🎮 Live Graph Lab")
    c1, c2 = st.columns([1, 2])
    with c1:
        ftype = st.selectbox("Function", ["Sine", "Cosine", "Tangent"])
        a = st.slider("Amplitude (a)", 0.1, 5.0, 1.0)
        q = st.slider("Vertical Shift (q)", -5.0, 5.0, 0.0)
    
    with c2:
        x = np.linspace(0, 360, 500)
        x_rad = np.radians(x)
        if ftype == "Sine": y = a * np.sin(x_rad) + q
        elif ftype == "Cosine": y = a * np.cos(x_rad) + q
        else: 
            y = a * np.tan(x_rad) + q
            y[np.abs(y) > 10] = np.nan
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, name="Result", line=dict(color='blue', width=3)))
        fig.add_hline(y=q, line_dash="dash", line_color="red")
        fig.update_layout(yaxis=dict(range=[-6, 6]), height=400)
        st.plotly_chart(fig, use_container_width=True)

def render_test_static():
    t_set = ALL_TEST_SETS[st.session_state.current_test_set_index]
    st.header("Trig Assessment")
    
    if st.session_state.show_grade_result:
        st.success(f"Graded! Last Score: {st.session_state.last_submission_score}")

    with st.form("test_form"):
        user_ans = []
        for i, q in enumerate(t_set["questions"]):
            st.latex(q["question"])
            user_ans.append(st.text_input(f"Your answer Q{i+1}", key=f"q{i}"))
        
        if st.form_submit_button("Submit"):
            correct = sum(1 for u, e in zip(user_ans, t_set["answers"]) if normalize_answer(u) == normalize_answer(e))
            score_str = f"{correct}/{len(user_ans)}"
            st.session_state.test_submissions.append({
                "Submission Time": datetime.datetime.now().strftime("%H:%M:%S"),
                "Score": score_str,
                "Percentage": (correct/len(user_ans))*100
            })
            st.session_state.last_submission_score = score_str
            st.session_state.show_grade_result = True
            st.rerun()

def render_analytics_page():
    st.header("Performance History")
    if not st.session_state.test_submissions:
        st.info("No tests taken yet!")
    else:
        df = pd.DataFrame(st.session_state.test_submissions)
        st.line_chart(df, x="Submission Time", y="Percentage")
        st.dataframe(df, use_container_width=True)

def render_rule_examples(page_data):
    rid = page_data["rule_id"]
    rule = next(r for r in RULES_DATA if r["id"] == rid)
    st.header(rule["name"])
    st.latex(rule["formula"])
    for q, a in RULE_EXAMPLE_SETS[rid][0]:
        with st.container(border=True):
            st.latex(q)
            st.write(f"Result: {a}")

def render_practice_interactive():
    prob = INTERACTIVE_PROBLEM_SETS[0]
    st.header(prob["title"])
    st.latex(prob["problem_latex"])
    
    if "p_step" not in st.session_state: st.session_state.p_step = 0
    
    for i, step in enumerate(prob["skeleton"]):
        if i <= st.session_state.p_step:
            st.latex(step["step_latex"])
            if step["correct_rule"] and i == st.session_state.p_step:
                opts = ["--Select--"] + [f"{r['id']}: {r['name']}" for r in RULES_DATA]
                choice = st.selectbox("Identify the rule:", opts, key=f"step{i}")
                if st.button("Check Step"):
                    if choice.startswith(step["correct_rule"]):
                        st.session_state.p_step += 1
                        st.rerun()
                    else: st.error("Try again!")

# -------------------------
# MAIN INITIALIZATION
# -------------------------
def main():
    # Fix the AttributeErrors by ensuring these exist before ANY page renders
    if 'test_submissions' not in st.session_state:
        st.session_state.test_submissions = []
    if 'show_grade_result' not in st.session_state:
        st.session_state.show_grade_result = False
    if 'last_submission_score' not in st.session_state:
        st.session_state.last_submission_score = ""
    if 'current_test_set_index' not in st.session_state:
        st.session_state.current_test_set_index = 0

    sel = st.sidebar.radio("Navigation", list(LESSON_PAGES.keys()))
    page = LESSON_PAGES[sel]
    pt = page["type"]

    if pt == "theory_summary": render_rules_overview()
    elif pt == "rule_examples": render_rule_examples(page)
    elif pt == "practice_interactive": render_practice_interactive()
    elif pt == "test_static": render_test_static()
    elif pt == "analytics_page": render_analytics_page()
    elif pt == "visualization_tab": render_visualization_tab()

if __name__ == "__main__":
    main()

