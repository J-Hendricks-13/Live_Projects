import streamlit as st
import pandas as pd
import random
from math import ceil
import datetime

st.set_page_config(page_title="Trig & Graph Interpreter", layout="wide")

# -------------------------
# DATA: TRIGONOMETRY & GRAPHS
# -------------------------
RULES_DATA = [
    {
        "id": "TRIG_01",
        "name": "Amplitude (a)",
        "description": "The 'a' value affects the vertical stretch. It is half the distance between the max and min values.",
        "formula": r"a = \frac{\text{max} - \text{min}}{2}",
    },
    {
        "id": "TRIG_02",
        "name": "Vertical Shift (q)",
        "description": "The 'q' value shifts the entire graph up or down. It represents the new rest position (equilibrium line).",
        "formula": r"q = \frac{\text{max} + \text{min}}{2}",
    },
    {
        "id": "TRIG_03",
        "name": "The Period",
        "description": "The distance (in degrees) for the graph to complete one full cycle. For sin/cos, it's 360°; for tan, it's 180°.",
        "formula": r"\text{Period of } \sin(kx) = \frac{360^\circ}{k}",
    },
    {
        "id": "TRIG_04",
        "name": "The Tangent Asymptote",
        "description": "The tan graph is undefined where the cosine is zero. These vertical lines are called asymptotes.",
        "formula": r"x = 90^\circ + k \cdot 180^\circ",
    },
]

RULE_EXAMPLE_SETS = {
    "TRIG_01": [
        [
            (r"y = 3\sin(x)", r"a = 3, \text{ Range: } [-3, 3]"),
            (r"y = -2\cos(x)", r"a = 2 \text{ (reflected across x-axis)}"),
        ],
        [
            (r"y = \frac{1}{2}\sin(x)", r"a = 0.5, \text{ Range: } [-0.5, 0.5]"),
        ]
    ],
    "TRIG_02": [
        [
            (r"y = \sin(x) + 2", r"q = 2, \text{ Graph moves up 2 units.}"),
            (r"y = \cos(x) - 5", r"q = -5, \text{ Graph moves down 5 units.}"),
        ]
    ]
}

INTERACTIVE_PROBLEM_SETS = [
    {
        "title": "Interpreting y = a sin(x) + q",
        "problem_latex": r"\text{A sine graph has a max of 5 and a min of 1. Find the equation.}",
        "skeleton": [
            {"step_latex": r"\text{Calculate amplitude: } a = \frac{5 - 1}{2}", "correct_rule": "TRIG_01",},
            {"step_latex": r"\text{Calculate shift: } q = \frac{5 + 1}{2}", "correct_rule": "TRIG_02",},
            {"step_latex": r"\text{Final Equation: } y = 2\sin(x) + 3", "correct_rule": None,},
        ],
    },
]

ALL_TEST_SETS = [
    {
        "questions": [
            {
                "question": r"\text{Range of } y = 3\cos(x) + 1?",
                "solution_steps": [r"\text{Amp = 3, Shift = 1}", r"\text{Max: } 1+3=4, \text{ Min: } 1-3=-2", r"\text{Final: } [-2, 4]"],
            },
            {
                "question": r"\text{Period of } y = \sin(2x)?",
                "solution_steps": [r"\text{Formula: } 360/k", r"360/2 = 180^\circ"],
            },
            {
                "question": r"\text{Value of } \tan(45^\circ)?",
                "solution_steps": [r"\text{Special angles: } 1"],
            },
        ],
        "answers": [r"[-2,4]", r"180", r"1"],
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
# HELPERS (Same Logic as your Template)
# -------------------------
def get_rule_by_id(rid):
    return next((r for r in RULES_DATA if r["id"] == rid), None)

def get_random_examples(rule_id):
    sets = RULE_EXAMPLE_SETS.get(rule_id, [])
    if not sets: return []
    session_key = f"examples_{rule_id}_set_index"
    if session_key not in st.session_state:
        st.session_state[session_key] = random.randrange(len(sets))
    return sets[st.session_state[session_key]]

def get_practice_problem():
    session_key = "practice_problem_index"
    if session_key not in st.session_state:
        st.session_state[session_key] = random.randrange(len(INTERACTIVE_PROBLEM_SETS))
    return INTERACTIVE_PROBLEM_SETS[st.session_state[session_key]]

def get_current_test_set():
    session_key = "current_test_set_index"
    if session_key not in st.session_state:
        st.session_state[session_key] = random.randrange(len(ALL_TEST_SETS))
    return ALL_TEST_SETS[st.session_state[session_key]], st.session_state[session_key]

def rotate_test_set():
    current_index = st.session_state.get("current_test_set_index", 0)
    new_index = (current_index + 1) % len(ALL_TEST_SETS)
    st.session_state["current_test_set_index"] = new_index
    st.session_state.user_test_answers = [""] * len(ALL_TEST_SETS[new_index]["questions"])

def normalize_answer(ans):
    return str(ans).replace(' ', '').lower().strip()

def submit_test_score(user_answers, expected_answers, total_questions):
    correct_count = 0
    graded_answers = []
    for i, user_ans in enumerate(user_answers):
        is_correct = normalize_answer(user_ans) == normalize_answer(expected_answers[i])
        if is_correct: correct_count += 1
        graded_answers.append(f"Q{i+1}: {'✅' if is_correct else '❌'}")
    
    percentage = ceil((correct_count / total_questions) * 100)
    st.session_state.test_submissions.append({
        "Submission Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Score": f"{correct_count}/{total_questions}",
        "Percentage": f"{percentage}%",
        "Detailed Feedback": " | ".join(graded_answers)
    })
    st.session_state.last_submission_score = f"{correct_count}/{total_questions}"
    st.session_state.show_grade_result = True
    rotate_test_set()
    st.rerun()

# -------------------------
# RENDERERS
# -------------------------
def render_rules_overview():
    st.header("📈 Trigonometry & Graph Interpretation")
    st.info("Grade 11 focus: Understanding how parameters change the shape of the wave.")
    
    # Insert visual aid for Sine/Cosine/Tangent
    
    
    for r in RULES_DATA:
        with st.expander(f"{r['id']}: {r['name']}", expanded=True):
            st.latex(r["formula"])
            st.write(r["description"])

def render_rule_examples(page_data):
    rid = page_data.get("rule_id")
    rule = get_rule_by_id(rid)
    examples = get_random_examples(rid)
    if rule:
        st.header(f"Explaining {rule['name']}")
        st.latex(rule["formula"])
        for i, (q, a) in enumerate(examples, start=1):
            st.info(f"Example {i}")
            st.latex(f"f(x) = {q}")
            st.success(f"Interpretation: {a}")

def render_practice_interactive():
    prob = get_practice_problem()
    st.header(prob['title'])
    st.latex(prob["problem_latex"])
    
    if "practice_step" not in st.session_state:
        st.session_state.practice_step = 0
    
    skeleton = prob["skeleton"]
    for i, step in enumerate(skeleton):
        if i <= st.session_state.practice_step:
            st.latex(step["step_latex"])
            if step["correct_rule"]:
                options = ["-- Select --"] + [f"{r['id']} — {r['name']}" for r in RULES_DATA]
                choice = st.selectbox(f"Which rule is being used in Step {i+1}?", options, key=f"p_{i}")
                if st.button("Verify Step", key=f"b_{i}"):
                    if choice.split(" — ")[0] == step["correct_rule"]:
                        st.session_state.practice_step += 1
                        st.rerun()
                    else:
                        st.error("Try again! Look at the formula used.")
            else:
                if i == st.session_state.practice_step and i < len(skeleton)-1:
                    if st.button("Next Step"):
                        st.session_state.practice_step += 1
                        st.rerun()

def render_test_static():
    current_test_set, set_index = get_current_test_set()
    st.header(f"Graded Assessment (Set {set_index + 1})")
    
    if st.session_state.show_grade_result:
        st.balloons()
        st.success(f"Last Score: {st.session_state.last_submission_score}")
        st.session_state.show_grade_result = False

    with st.form("trig_test"):
        for i, q in enumerate(current_test_set["questions"]):
            st.latex(q["question"])
            st.text_input("Your Answer", key=f"ans_{i}")
        if st.form_submit_button("Submit Answers"):
            # Simplified for demo: pull answers from session state
            user_ans = [st.session_state[f"ans_{i}"] for i in range(len(current_test_set["questions"]))]
            submit_test_score(user_ans, current_test_set["answers"], len(user_ans))

def render_analytics_page():
    st.header("Analytics")
    if st.session_state.test_submissions:
        df = pd.DataFrame(st.session_state.test_submissions)
        df['ScoreVal'] = df['Percentage'].str.replace('%','').astype(int)
        st.line_chart(df, x="Submission Time", y="ScoreVal")
        st.table(df)
    else:
        st.write("No data yet.")

# -------------------------
# MAIN
# -------------------------
def render_visualization_tab():
    st.header("🎮 Live Graph Lab")
    st.markdown("Adjust the sliders to see how the parameters **$a$** and **$q$** transform the parent function.")

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("Controls")
        func_type = st.selectbox("Select Function", ["Sine", "Cosine", "Tangent"])
        a = st.slider("Amplitude (a)", float(0.5), float(5.0), float(1.0), 0.5)
        q = st.slider("Vertical Shift (q)", float(-5.0), float(5.0), float(0.0), 0.5)
        
        st.info(f"Current Equation: \n\n $y = {a} \\, \\text{{{func_type.lower()}}}(x) + ({q})$")

    with col2:
        # Generate Data
        x = np.linspace(0, 360, 500)
        x_rad = np.radians(x)
        
        if func_type == "Sine":
            y = a * np.sin(x_rad) + q
        elif func_type == "Cosine":
            y = a * np.cos(x_rad) + q
        else: # Tangent
            y = a * np.tan(x_rad) + q
            # Clean up Tan asymptotes for better plotting
            y[np.abs(y) > 10] = np.nan 

        # Create Plotly Chart
        fig = go.Figure()
        
        # Add the transformed graph
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f'Transformed {func_type}', line=dict(color='firebrick', width=3)))
        
        # Add Reference Line (Rest Position / q)
        fig.add_hline(y=q, line_dash="dash", line_color="gray", annotation_text="Rest Position (q)")

        fig.update_layout(
            title=f"Interactive {func_type} Graph",
            xaxis_title="Degrees (°)",
            yaxis_title="y",
            yaxis=dict(range=[-7, 7]),
            xaxis=dict(tickmode='array', tickvals=[0, 90, 180, 270, 360]),
            template="plotly_white",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Update the main() logic to handle the new ptype
def main():
    # ... (state initialization)
    
    sel = st.sidebar.radio("Navigate Lesson", list(LESSON_PAGES.keys()))
    page = LESSON_PAGES[sel]
    ptype = page.get("type")

    if ptype == "theory_summary": render_rules_overview()
    elif ptype == "rule_examples": render_rule_examples(page)
    elif ptype == "practice_interactive": render_practice_interactive()
    elif ptype == "test_static": render_test_static()
    elif ptype == "analytics_page": render_analytics_page()
    elif ptype == "visualization_tab": render_visualization_tab() # NEW

if __name__ == "__main__":
    main()
