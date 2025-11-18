import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="SQL Join Visualizer", layout="wide")

# =======================
# DATA (Expanded)
# =======================
A = pd.DataFrame({
    'EmployeeID': [101, 102, 103, 104, 105],
    'Employee': ['Jawaad', 'Sarah', 'Thabo', 'Lerato', 'Imran'],
    'DepartmentID': [10, 20, 10, 30, 40],
    'City': ['JHB', 'CPT', 'JHB', 'DBN', 'CPT'],
    'HireDate': ['2020-01-10', '2021-05-22', '2019-08-04', '2022-11-03', '2020-03-30'],
    'Salary': [55000, 62000, 50000, 70000, 58000],
    'ManagerID': [900, 900, 901, 901, 902]
})

B = pd.DataFrame({
    'DepartmentID': [10, 20, 30, 50],
    'Department': ['Finance', 'IT', 'Logistics', 'Marketing'],
    'Location': ['JHB', 'CPT', 'DBN', 'JHB'],
    'Budget': [200000, 350000, 150000, 500000],
    'HeadOfDepartment': ['Alice', 'Ben', 'Cheryl', 'Daniel']
})


# Define clear, high-contrast colours
COLOR_LEFT_ONLY = '#ffc0cb'  # Light Pink/Coral - Exclusive to A
COLOR_RIGHT_ONLY = '#add8e6' # Light Blue/Sky Blue - Exclusive to B
COLOR_BOTH = '#90ee90'       # Light Green/Pale Green - Intersection

# =======================
# FUNCTIONS
# =======================
def do_join(join_type, key_A, key_B):
    """Performs the merge operation using the user-selected join keys."""
    # Use left_on and right_on to join on specific columns, instead of the index
    return A.merge(B, left_on=key_A, right_on=key_B, how=join_type.lower(), indicator=True)

def highlight_rows(row):
    """Highlights rows based on the join result type using high-contrast colours."""
    if row['_merge'] == "left_only":
        return [f'background-color: {COLOR_LEFT_ONLY}'] * len(row)
    elif row['_merge'] == "right_only":
        return [f'background-color: {COLOR_RIGHT_ONLY}'] * len(row)
    else: # 'both'
        return [f'background-color: {COLOR_BOTH}'] * len(row)

def get_join_explanation(join_type, key_A, key_B):
    """Provides the educational explanation for the selected join."""
    base_notes = {
        "INNER": "Returns records where the value in Table A's **{}** matches the value in Table B's **{}**.".format(key_A, key_B),
        "LEFT": "Returns **all** records from the **LEFT** table (A) and matched records from B. Unmatched fields from B show **NaN**.",
        "RIGHT": "Returns **all** records from the **RIGHT** table (B) and matched records from A. Unmatched fields from A show **NaN**.",
        "OUTER": "Returns **all** records when there is a match in either table. Unmatched fields from both tables show **NaN**.",
    }
    return base_notes.get(join_type, "")

def draw_venn(join_type, left_only, both, right_only):
    """Draws a simplified Venn diagram and shades the region based on the join type."""
    fig = go.Figure()
    
    # 1. Define base shapes (Circles)
    fig.add_shape(type="circle", x0=0, y0=0, x1=2, y1=2, line_color="DarkBlue", line_width=2, opacity=0.1, fillcolor='rgba(0, 0, 255, 0.1)')
    fig.add_shape(type="circle", x0=1, y0=0, x1=3, y1=2, line_color="DarkRed", line_width=2, opacity=0.1, fillcolor='rgba(255, 0, 0, 0.1)')

    # 2. Define Shading based on Join Type (using approximations for regions)
    if join_type == "INNER":
        # Shade the intersection region (approx. x=1 to x=2)
        shades = [dict(x0=1, y0=0, x1=2, y1=2, color=COLOR_BOTH)]
    elif join_type == "LEFT":
        # Shade Left Exclusive (approx. x=0 to x=1) and Intersection (x=1 to x=2)
        shades = [
            dict(x0=0, y0=0, x1=1, y1=2, color=COLOR_LEFT_ONLY),
            dict(x0=1, y0=0, x1=2, y1=2, color=COLOR_BOTH)
        ]
    elif join_type == "RIGHT":
        # Shade Intersection (x=1 to x=2) and Right Exclusive (x=2 to x=3)
        shades = [
            dict(x0=1, y0=0, x1=2, y1=2, color=COLOR_BOTH),
            dict(x0=2, y0=0, x1=3, y1=2, color=COLOR_RIGHT_ONLY)
        ]
    elif join_type == "OUTER":
        # Shade all three regions
        shades = [
            dict(x0=0, y0=0, x1=1, y1=2, color=COLOR_LEFT_ONLY),
            dict(x0=1, y0=0, x1=2, y1=2, color=COLOR_BOTH),
            dict(x0=2, y0=0, x1=3, y1=2, color=COLOR_RIGHT_ONLY)
        ]
    else:
        shades = []

    # Apply shading shapes
    for s in shades:
        fig.add_shape(type="rect", xref="x", yref="y", x0=s['x0'], y0=s['y0'], x1=s['x1'], y1=s['y1'],
                      fillcolor=s['color'], opacity=0.7, layer="below", line_width=0)


    # 3. Add Counts and Labels
    # Plotly text coordinates are centered, so we adjust x slightly
    fig.add_trace(go.Scatter(x=[0.5], y=[1], text=[f"A Only<br>({left_only})"], mode="text", textfont=dict(size=14, color='black')))
    fig.add_trace(go.Scatter(x=[1.5], y=[1], text=[f"Both<br>({both})"], mode="text", textfont=dict(size=14, color='black')))
    fig.add_trace(go.Scatter(x=[2.5], y=[1], text=[f"B Only<br>({right_only})"], mode="text", textfont=dict(size=14, color='black')))

    fig.update_xaxes(visible=False, range=[-0.5, 3.5])
    fig.update_yaxes(visible=False, range=[-0.5, 2.5])
    fig.update_layout(height=350, width=550, showlegend=False, template='plotly_white', margin=dict(l=20, r=20, t=20, b=20))

    return fig

# =======================
# LAYOUT
# =======================
st.title("SQL Join Visualizer 💾")

st.markdown("### 1. Select Tables and Join Keys")
key_col, left_col, right_col = st.columns([1, 2, 2])

with key_col:
    st.markdown("##### Join Key Selection")
    # User selects the column to join on for each table
    join_key_A = st.selectbox("Key Column (Table A):", A.columns.tolist(), index=0)
    join_key_B = st.selectbox("Key Column (Table B):", B.columns.tolist(), index=0)

with left_col:
    st.subheader("Table A (Employees)")
    st.dataframe(A, use_container_width=True)

with right_col:
    st.subheader("Table B (Departments)")
    st.dataframe(B, use_container_width=True)

st.divider()

# --- Join Selection and Execution ---
st.markdown("### 2. Select Join Type and View Result")
join_type = st.radio("Choose Join Type", ["INNER", "LEFT", "RIGHT", "OUTER"], horizontal=True)

# -----------------
# PROCESSING
# -----------------
result = do_join(join_type, join_key_A, join_key_B)

# Count venn sections
left_only = (result["_merge"] == "left_only").sum()
right_only = (result["_merge"] == "right_only").sum()
both = (result["_merge"] == "both").sum()

st.subheader(f"{join_type} JOIN Result (on A.{join_key_A} = B.{join_key_B})")

# Display Educational Notes and Legend
st.markdown(f"**Explanation:** {get_join_explanation(join_type, join_key_A, join_key_B)}")
st.caption("Rows are highlighted based on the origin of the join:")
st.markdown(f"<span style='background-color: {COLOR_BOTH}'>&nbsp;&nbsp;&nbsp;&nbsp;</span> **Green:** Intersection (matched records)", unsafe_allow_html=True)
st.markdown(f"<span style='background-color: {COLOR_LEFT_ONLY}'>&nbsp;&nbsp;&nbsp;&nbsp;</span> **Pink:** Left Only (unmatched in B)", unsafe_allow_html=True)
st.markdown(f"<span style='background-color: {COLOR_RIGHT_ONLY}'>&nbsp;&nbsp;&nbsp;&nbsp;</span> **Blue:** Right Only (unmatched in A)", unsafe_allow_html=True)

# Display Styled DataFrame
# --- Fix Applied Here ---

# 1. Apply the style (which needs the '_merge' column).
styled = result.style.apply(highlight_rows, axis=1)

# 2. THEN, hide the '_merge' column from the final display.
st.dataframe(styled.hide(subset=['_merge'], axis=1), use_container_width=True)

st.divider()

# Display Visual Diagram
st.markdown("### 3. Venn Diagram Visualization")
st.plotly_chart(draw_venn(join_type, left_only, both, right_only))