import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime

# =====================================================
# CONFIGURATION
# =====================================================
st.set_page_config(page_title="Ultimate Math Tutor", layout="wide")

EPS = 1e-6
Y_CLIP = 1e3


# =====================================================
# SESSION STATE MANAGEMENT
# =====================================================
def init_session_state():
    defaults = {
        "test_submissions": [],
        "show_grade_result": False,
        "last_score": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# =====================================================
# MATHEMATICAL MODELS
# =====================================================
def generate_parabola(a, q):
    x = np.linspace(-10, 10, 400)
    y = a * (x**2) + q
    return x, y


def generate_hyperbola(a, q):
    x = np.linspace(-10, 10, 400)
    x = x[np.abs(x) > EPS]
    y = (a / x) + q
    return x, y


def generate_exponential(a, b, q):
    x = np.linspace(-5, 5, 400)
    y = a * np.power(b, x)
    y = np.clip(y, -Y_CLIP, Y_CLIP) + q
    return x, y


def generate_sine(a, q):
    x = np.linspace(0, 360, 500)
    y = a * np.sin(np.radians(x)) + q
    return x, y


# =====================================================
# GRADING ENGINE
# =====================================================
def normalize(text):
    return text.replace(" ", "").lower()


def grade_assessment(ans1, ans2):
    score = 0

    if normalize(ans1) in ["(0,2)", "0,2"]:
        score += 1

    if normalize(ans2) in ["y=-4", "-4"]:
        score += 1

    return score


# =====================================================
# VISUALIZATION ENGINE
# =====================================================
def plot_graph(x, y, q):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, line=dict(width=3)))
    fig.add_hline(y=q, line_dash="dash", annotation_text=f"y = {q}")
    fig.update_layout(template="plotly_white", height=500, yaxis=dict(range=[-10, 10]))
    return fig


# =====================================================
# LESSON RENDERERS
# =====================================================
def render_theory():
    st.header("Function Gallery")

    functions = [
        ("Parabola", r"y = ax^2 + q", "Turning point at (0, q)"),
        ("Hyperbola", r"y = \frac{a}{x} + q", "Asymptotes x=0 and y=q"),
        ("Exponential", r"y = a \cdot b^x + q", "Horizontal asymptote y=q"),
        ("Sine", r"y = a\sin(x) + q", "Amplitude a, midline q"),
    ]

    cols = st.columns(2)
    for i, f in enumerate(functions):
        with cols[i % 2]:
            with st.container(border=True):
                st.subheader(f[0])
                st.latex(f[1])
                st.write(f[2])


def render_graph_lab():
    st.header("Graph Lab")

    col1, col2 = st.columns([1, 2])

    with col1:
        func = st.selectbox("Function", ["Parabola", "Hyperbola", "Exponential", "Sine"])
        a = st.slider("Stretch (a)", -5.0, 5.0, 1.0, 0.5)
        q = st.slider("Shift (q)", -5.0, 5.0, 0.0, 0.5)

        if func == "Exponential":
            b = st.radio("Base (b)", [2.0, 0.5])
        else:
            b = None

        st.markdown("### Interpretation")

        if func == "Parabola":
            st.write(f"Turning point: (0, {q})")
            st.write("Opens upward" if a > 0 else "Opens downward")

        elif func == "Hyperbola":
            st.write("Vertical asymptote: x = 0")
            st.write(f"Horizontal asymptote: y = {q}")

        elif func == "Exponential":
            st.write("Growth" if b > 1 else "Decay")
            st.write(f"Asymptote y = {q}")

        elif func == "Sine":
            st.write(f"Amplitude = {abs(a)}")
            st.write(f"Midline y = {q}")

    with col2:
        if func == "Parabola":
            x, y = generate_parabola(a, q)

        elif func == "Hyperbola":
            x, y = generate_hyperbola(a, q)

        elif func == "Exponential":
            x, y = generate_exponential(a, b, q)

        else:
            x, y = generate_sine(a, q)

        st.plotly_chart(plot_graph(x, y, q), use_container_width=True)


def render_assessment():
    st.header("Assessment")

    if st.session_state.show_grade_result:
        st.success(f"Score: {st.session_state.last_score}")

    with st.form("assessment_form"):
        st.write("Q1: If y = 3x² + 2, what is the turning point?")
        ans1 = st.text_input("Answer Q1")

        st.write("Q2: In y = 2/x - 4, what is the horizontal asymptote?")
        ans2 = st.text_input("Answer Q2")

        if st.form_submit_button("Submit"):
            correct = grade_assessment(ans1, ans2)
            percent = (correct / 2) * 100

            st.session_state.test_submissions.append({
                "Time": datetime.datetime.now().strftime("%H:%M"),
                "Score": f"{correct}/2",
                "Percent": percent
            })

            st.session_state.last_score = f"{correct}/2"
            st.session_state.show_grade_result = True
            st.rerun()


def render_analytics():
    st.header("Progress Analytics")

    if not st.session_state.test_submissions:
        st.info("No results yet.")
        return

    df = pd.DataFrame(st.session_state.test_submissions)
    st.line_chart(df, x="Time", y="Percent")
    st.dataframe(df, use_container_width=True)

    avg = df["Percent"].mean()
    st.metric("Average Score", f"{avg:.1f}%")

    if avg < 60:
        st.warning("Student needs reinforcement.")


# =====================================================
# APP ROUTER
# =====================================================
def main():
    init_session_state()

    st.sidebar.title("Tutor System")
    page = st.sidebar.radio("Navigation", [
        "Theory",
        "Graph Lab",
        "Assessment",
        "Analytics"
    ])

    if page == "Theory":
        render_theory()

    elif page == "Graph Lab":
        render_graph_lab()

    elif page == "Assessment":
        render_assessment()

    elif page == "Analytics":
        render_analytics()


if __name__ == "__main__":
    main()
