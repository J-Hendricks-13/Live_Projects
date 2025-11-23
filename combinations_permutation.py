import streamlit as st
import math

# --- App Configuration ---
st.set_page_config(
    page_title="Permutations & Combinations Lesson",
    layout="wide",
    initial_sidebar_state="expanded"
)

## --- Mathematical Functions (Kept for calculator/solver pages) ---
def combinations(n, k):
    """Calculates C(n, k)."""
    if k < 0 or k > n:
        return 0
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

def permutations(n, k):
    """Calculates P(n, k)."""
    if k < 0 or k > n:
        return 0
    return math.factorial(n) // math.factorial(n - k)

def stars_and_bars(n, k):
    """Calculates Stars and Bars (ways to place n identical items into k distinct bins)."""
    # Formula for non-negative integer solutions: C(n + k - 1, k - 1)
    return combinations(n + k - 1, k - 1)

## --- Streamlit UI Components ---
def display_header():
    """Sets up the main header for the application."""
    st.title("🧮 Permutations & Combinations Interactive Lesson")
    st.markdown("""
    This tool is designed to help you understand the difference between permutations, combinations,
    and related counting techniques.
    """)
    st.sidebar.header("Navigation")

def display_explanation_page():
    """Displays the core concepts and formulas with corrected LaTeX."""
    st.sidebar.success("Viewing Core Concepts")
    st.header("1. Core Concepts & Formulas")

    # --- Permutations ---
    st.subheader("Permutations ($P(n, k)$)")
    st.markdown("""
    * **Definition:** The number of ways to arrange $k$ items chosen from a set of $n$ distinct items.
    * **Order Matters:** *Arrangement* or *Order* is important (e.g., a podium finish, forming a word).
    """)
    # Corrected LaTeX for Permutations
    st.latex(r"P(n, k) = \frac{n!}{(n - k)!}")

    # --- Combinations ---
    st.subheader("Combinations ($C(n, k)$)")
    st.markdown("""
    * **Definition:** The number of ways to choose a subset of $k$ items from a set of $n$ distinct items.
    * **Order Doesn't Matter:** *Selection* or *Group* is formed (e.g., choosing a committee, picking lottery numbers).
    """)
    # Corrected LaTeX for Combinations
    st.latex(r"C(n, k) = \binom{n}{k} = \frac{n!}{k!(n - k)!}")

    # --- Stars and Bars ---
    st.subheader("Stars and Bars (Identical Items / Distinct Bins)")
    st.markdown("""
    * **Definition:** The number of ways to distribute $n$ identical items into $k$ distinct bins (non-negative solutions to $x_1 + x_2 + \dots + x_k = n$).
    """)
    # Corrected LaTeX for Stars and Bars
    st.latex(r"\text{Ways} = \binom{n + k - 1}{k - 1}")


def display_calculator_page():
    """Displays an interactive calculator for students to explore."""
    st.sidebar.info("Viewing Interactive Calculator")
    st.header("2. Interactive Calculator")
    st.write("Explore how changing $n$ (total items) and $k$ (chosen items/bins) affects the result.")

    col1, col2 = st.columns(2)
    with col1:
        n = st.slider("Total Items (n):", min_value=0, max_value=15, value=5)
    with col2:
        k = st.slider("Items Chosen/Bins (k):", min_value=0, max_value=max(1, n), value=3)

    st.markdown("---")

    st.subheader("Permutations (Order Matters)")
    perm_result = permutations(n, k)
    # Using raw string for latex to handle backslashes better
    st.latex(r"P(%d, %d) = \frac{%d!}{(%d - %d)!} = %d" % (n, k, n, n, k, perm_result))
    st.metric(label=f"P({n}, {k}) Result:", value=f"{perm_result}")

    st.subheader("Combinations (Order Doesn't Matter)")
    comb_result = combinations(n, k)
    st.latex(r"C(%d, %d) = \frac{%d!}{%d!(%d - %d)!} = %d" % (n, k, n, k, n, k, comb_result))
    st.metric(label=f"C({n}, {k}) Result:", value=f"{comb_result}")

    st.subheader("Stars and Bars (Identical Items, Distinct Bins)")
    sb_result = stars_and_bars(n, k)
    # n is items (stars), k is bins (dividers)
    st.latex(r"\text{Ways} = \binom{%d + %d - 1}{%d - 1} = \binom{%d}{%d} = %d" % (n, k, k, n + k - 1, k - 1, sb_result))
    st.metric(label=f"Ways to distribute {n} identical items into {k} bins:", value=f"{sb_result}")

def display_problem_solver():
    """Displays a section to solve one of the user's provided problems."""
    st.sidebar.warning("Viewing Problem Solver")
    st.header("3. Step-by-Step Problem Solver")
    
    # Example problem selected from the user's list
    st.subheader("Example: Problem 18 - Permutations")
    st.markdown("""
    **Problem:** How many 3-letter "words" can be formed from the letters A, B, C, D, E if letters cannot be repeated?
    """)

    st.info("Ask yourself: **Does the order of the letters matter?** Yes, 'ABC' is different from 'BCA'. This is a **Permutation**.")

    n_val = 5
    k_val = 3
    
    st.markdown(f"* Total letters ($n$): **{n_val}**")
    st.markdown(f"* Letters to be chosen/arranged ($k$): **{k_val}**")
    
    final_result = permutations(n_val, k_val)
    
    st.latex(r"P(5, 3) = \frac{5!}{( 5 - 3 )!} = \frac{5!}{2!} = 5 \times 4 \times 3 = 60")
    st.metric(label="Final Answer:", value=f"{final_result}", help="Corresponds to answer B. 60 from your list.")

    st.subheader("Example: Problem 16 - Combinations")
    st.markdown("""
    **Problem:** In how many ways can you choose 3 different fruits from a basket containing 5 different fruits?
    """)

    st.info("Ask yourself: **Does the order of choosing the fruits matter?** No, choosing {Apple, Banana, Cherry} is the same as {Cherry, Apple, Banana}. This is a **Combination**.")

    n_val = 5
    k_val = 3
    
    st.markdown(f"* Total fruits ($n$): **{n_val}**")
    st.markdown(f"* Fruits to be chosen ($k$): **{k_val}**")
    
    final_result = combinations(n_val, k_val)
    
    st.latex(r"C(5, 3) = \frac{5!}{3!( 5 - 3 )!} = \frac{5!}{3!2!} = \frac{5 \times 4}{2 \times 1} = 10")
    st.metric(label="Final Answer:", value=f"{final_result}", help="Corresponds to answer B. 10 from your list.")


# --- Main Application Logic ---
def main():
    display_header()
    
    # Use radio buttons in the sidebar for navigation
    lesson_part = st.sidebar.radio(
        "Select Lesson Part:",
        ("Core Concepts", "Interactive Calculator", "Problem Solver")
    )
    
    if lesson_part == "Core Concepts":
        display_explanation_page()
    elif lesson_part == "Interactive Calculator":
        display_calculator_page()
    elif lesson_part == "Problem Solver":
        display_problem_solver()

if __name__ == "__main__":
    main()