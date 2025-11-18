# tutor_simulator.py
"""
Tutor Time Management Simulation
Single-file Streamlit app.

Run: streamlit run tutor_simulator.py
"""

import streamlit as st
import pandas as pd
import random
from math import ceil

# -------------------------
# DEFAULT CONFIG & COLORS
# -------------------------
DEFAULT_START_HOUR = 8
DEFAULT_END_HOUR = 17 # exclusive, e.g., 8..16 => 9 hours
DEFAULT_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]

L1_RATE = 100
L2_RATE = 200

# Color map for the timetable (must be CSS hex codes)
COLOR_FREE = '#F5F5F5'  # Light Grey
COLOR_L1 = '#ADD8E6' # Light Blue (Less revenue)
COLOR_L2 = '#FFD700' # Gold (High revenue)

# -------------------------
# UTIL / INIT
# -------------------------
st.set_page_config(page_title="Tutor Time Simulator", layout="wide")
st.title("Tutor Business Simulation — Timetable & Clients")

def init_schedule():
    """Initializes a clean schedule dict based on current hour settings."""
    schedule = {}
    hours = list(range(st.session_state.start_hour, st.session_state.end_hour))
    for day in st.session_state.days:
        for h in hours:
            schedule[(day, h)] = {"status": "free", "client_id": None}
    return schedule

def reset_state():
    """Reset dynamic simulation state and rebuild the schedule."""
    st.session_state.clients = [] # list of dicts
    st.session_state.metrics = {
        "total_revenue": 0.0,
        "current_week_hours": 0,
        "week_day_index": 0 # which day in week to simulate next
    }
    st.session_state.schedule = init_schedule()
    st.session_state.next_client_id = 1
    st.session_state.last_sim_results = [] # Store results for feedback

def init_session():
    """Initialize session_state defaults."""
    if "inited" not in st.session_state:
        st.session_state.inited = True
        st.session_state.start_hour = DEFAULT_START_HOUR
        st.session_state.end_hour = DEFAULT_END_HOUR
        st.session_state.days = DEFAULT_DAYS.copy()
        st.session_state.weekly_goal = 20 # hours target per week
        st.session_state.acquisition_rate = 0.6
        st.session_state.daily_acq_attempts = 2
        st.session_state.reschedule_chance = 0.7
        st.session_state.max_reschedules = 2
        st.session_state.allow_replacement = True
        st.session_state.next_client_id = 1
        st.session_state.last_sim_results = []
        reset_state()


# -------------------------
# MODEL BUILDERS & HELPERS
# -------------------------
def get_client_info(cid):
    """Retrieves client object from state"""
    return next((c for c in st.session_state.clients if c["id"] == cid), None)

def timeslot_to_display(cell):
    """Return display str for a slot"""
    if cell["status"] == "free":
        return ""
    cid = cell["client_id"]
    client = get_client_info(cid)
    if client:
        prefix = "L2" if client["level"] == 2 else "L1"
        return f"{prefix} | ID {cid}"
    return "ERROR"

def schedule_to_dataframe():
    """Convert internal schedule dict to a DataFrame for display"""
    hours = list(range(st.session_state.start_hour, st.session_state.end_hour))
    # Handle the case where start_hour >= end_hour, returning an empty DF
    if st.session_state.start_hour >= st.session_state.end_hour:
        return pd.DataFrame(columns=st.session_state.days)
        
    df = pd.DataFrame(index=[f"{h:02d}:00" for h in hours], columns=st.session_state.days)
    for day in st.session_state.days:
        for h in hours:
            if (day, h) in st.session_state.schedule:
                cell = st.session_state.schedule[(day, h)]
                df.at[f"{h:02d}:00", day] = timeslot_to_display(cell)
            else:
                df.at[f"{h:02d}:00", day] = "N/A" 
    return df

def create_client(level=1):
    cid = st.session_state.next_client_id
    st.session_state.next_client_id += 1
    client = {
        "id": cid,
        "level": level,
        "rate": L1_RATE if level == 1 else L2_RATE,
        "weekly_hours": 0,
        "active": True
    }
    st.session_state.clients.append(client)
    return client

def book_slot(day, hour, client):
    slot = st.session_state.schedule[(day, hour)]
    
    # 1. Handle potential removal of previous client's revenue/hours
    if slot["status"] != "free" and slot["client_id"] is not None:
        prev_client = get_client_info(slot["client_id"])
        if prev_client:
            st.session_state.metrics["current_week_hours"] -= 1
            st.session_state.metrics["total_revenue"] -= prev_client["rate"]
            prev_client["weekly_hours"] = max(0, prev_client["weekly_hours"] - 1)

    # 2. Assign the slot to the new client
    slot["status"] = "L2" if client["level"] == 2 else "L1"
    slot["client_id"] = client["id"]
    
    # 3. Update metrics for the new client
    client["weekly_hours"] += 1
    st.session_state.metrics["current_week_hours"] += 1
    st.session_state.metrics["total_revenue"] += client["rate"]

def attempt_booking_for_client(client, reschedule_limit=None, preferred_day=None):
    """Try to book a random slot for a client with reschedule attempts.
        Returns True if booked, False if lost/unable."""
    reschedule_limit = st.session_state.max_reschedules if reschedule_limit is None else reschedule_limit
    attempts = 0
    
    # Loop for the initial attempt (attempts=0) + reschedule_limit attempts
    while attempts <= reschedule_limit:
        # 1. Select proposed day and hour
        if preferred_day and random.random() < 0.6:
            day = preferred_day
        else:
            day = random.choice(st.session_state.days)
            
        hour = random.randint(st.session_state.start_hour, st.session_state.end_hour - 1)
        slot = st.session_state.schedule[(day, hour)]
        
        # 2. Check slot status
        if slot["status"] == "free":
            book_slot(day, hour, client)
            return True
            
        # 3. Conflict resolution (only if L2 client replacing L1)
        if client["level"] == 2 and slot["status"] == "L1" and st.session_state.allow_replacement:
            book_slot(day, hour, client)
            return True
            
        # 4. Failed attempt: Try reschedule if allowed
        
        # Increment attempt count here
        attempts += 1 

        if attempts <= reschedule_limit and random.random() < st.session_state.reschedule_chance:
            continue # Reschedule accepted, loop for new time
        else:
            # Reschedule denied or limit exceeded
            client["active"] = False
            return False
            
    client["active"] = False
    return False

# -------------------------
# SIMULATION LOGIC
# -------------------------
def roll_new_client():
    """Roll for creating a new client; level depends on progression"""
    if random.random() >= st.session_state.acquisition_rate:
        return None
        
    weekly_hours = st.session_state.metrics["current_week_hours"]
    goal = st.session_state.weekly_goal
    
    total_slots = len(st.session_state.schedule)
    is_nearly_full = (weekly_hours / total_slots) >= 0.8 if total_slots > 0 else False
    
    if is_nearly_full or weekly_hours >= 0.8 * goal:
        # 70% chance for L2 when near full capacity
        level = 2 if random.random() < 0.7 else 1
    else:
        level = 1
        
    return create_client(level=level)

def simulate_one_day():
    """Simulate attempts for one day (acquisition attempts per day configurable)"""
    day_idx = st.session_state.metrics["week_day_index"]
    if not st.session_state.days:
        return []
        
    current_day = st.session_state.days[day_idx % len(st.session_state.days)]
    results = []
    
    for _ in range(st.session_state.daily_acq_attempts):
        client = roll_new_client()
        if client is None:
            continue
            
        booked = attempt_booking_for_client(client, preferred_day=current_day)
        
        results.append({
            "day": current_day,
            "id": client["id"],
            "level": client["level"],
            "outcome": "Booked" if booked else "Lost"
        })
        
    st.session_state.metrics["week_day_index"] = (st.session_state.metrics["week_day_index"] + 1) % len(st.session_state.days)
    
    st.session_state.last_sim_results = results
    return results

def simulate_n_days(n):
    all_results = []
    for _ in range(n):
        all_results.extend(simulate_one_day())
    st.session_state.last_sim_results = all_results
    return all_results

# -------------------------
# UI CONTROLS & DISPLAY
# -------------------------
init_session()

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("Simulation Controls")
    
    st.caption("🚨 Changing hours resets the simulation.")
    
    start_h = st.number_input("Start hour (24h)", min_value=0, max_value=23, value=st.session_state.start_hour, key="ui_start_hour")
    end_h = st.number_input("End hour (24h, exclusive)", min_value=1, max_value=24, value=st.session_state.end_hour, key="ui_end_hour")
    
    if (start_h != st.session_state.start_hour or end_h != st.session_state.end_hour) and start_h < end_h:
        st.session_state.start_hour = int(start_h)
        st.session_state.end_hour = int(end_h)
        reset_state()
        st.rerun() 

    st.write("---")
    
    st.number_input("Weekly hours goal", min_value=1, max_value=168, value=st.session_state.weekly_goal, key="ui_week_goal")
    st.session_state.weekly_goal = int(st.session_state.ui_week_goal)

    st.slider("Acquisition probability (p new client per attempt)", 0.0, 1.0, value=st.session_state.acquisition_rate, step=0.05, key="ui_acq")
    st.session_state.acquisition_rate = float(st.session_state.ui_acq)

    st.number_input("Daily acquisition attempts", min_value=1, max_value=10, value=st.session_state.daily_acq_attempts, key="ui_daily_attempts")
    st.session_state.daily_acq_attempts = int(st.session_state.ui_daily_attempts)

    st.slider("Reschedule chance on conflict", 0.0, 1.0, value=st.session_state.reschedule_chance, step=0.05, key="ui_reschedule")
    st.session_state.reschedule_chance = float(st.session_state.ui_reschedule)

    st.number_input("Max reschedule attempts per client", min_value=0, max_value=10, value=st.session_state.max_reschedules, key="ui_max_res")
    st.session_state.max_reschedules = int(st.session_state.ui_max_res)

    st.checkbox("Allow L2 to replace L1 when full", value=st.session_state.allow_replacement, key="ui_replace")
    st.session_state.allow_replacement = bool(st.session_state.ui_replace)

    st.button("Reset Simulation", on_click=reset_state)

# --- 1. TOP METRICS DISPLAY ---
st.subheader("1. Business Metrics")
col_rev, col_hours, col_client_summary = st.columns([1.5, 1.5, 2])

with col_rev:
    st.metric("Total Revenue (R)", f"R {st.session_state.metrics['total_revenue']:.2f}")

with col_hours:
    total_slots = len(st.session_state.schedule)
    fill_percent = (st.session_state.metrics['current_week_hours'] / total_slots) * 100 if total_slots > 0 else 0
    st.metric("Weekly Hours Filled", f"{st.session_state.metrics['current_week_hours']}/{st.session_state.weekly_goal}")

with col_client_summary:
    l1_count = sum(1 for c in st.session_state.clients if c["level"] == 1 and c["active"])
    l2_count = sum(1 for c in st.session_state.clients if c["level"] == 2 and c["active"])
    st.markdown(f"**Level 1 Clients:** {l1_count}")
    st.markdown(f"**Level 2 Clients:** {l2_count}")

st.write("---")

# --- 2. TIMETABLE DISPLAY ---
st.subheader("2. Timetable")
st.markdown(f"**Legend:** <span style='background-color: {COLOR_L1}; padding: 2px 5px; border-radius: 3px;'>L1 (R{L1_RATE})</span> | <span style='background-color: {COLOR_L2}; padding: 2px 5px; border-radius: 3px;'>L2 (R{L2_RATE})</span> | <span style='background-color: {COLOR_FREE}; padding: 2px 5px; border-radius: 3px;'>FREE</span>", unsafe_allow_html=True)
display_df = schedule_to_dataframe()

def apply_background_color(cell_value):
    """Function to determine background color based on the cell content."""
    if pd.isna(cell_value) or cell_value == "" or "N/A" in cell_value:
        status = "free"
    elif "L1" in cell_value:
        status = "L1"
    elif "L2" in cell_value:
        status = "L2"
    else:
        status = "free"

    if status == "free":
        return f'background-color: {COLOR_FREE}'
    elif status == "L1":
        return f'background-color: {COLOR_L1}'
    elif status == "L2":
        return f'background-color: {COLOR_L2}'
    return None

st.dataframe(
    display_df.style.applymap(apply_background_color), 
    use_container_width=True
)

# --- 3. ACTIONS (NEW PLACEMENT) ---
st.write("---")
col_actions, col_status_msg = st.columns([1, 2])

with col_actions:
    st.subheader("3. Actions")
    day_of_week = st.session_state.days[st.session_state.metrics["week_day_index"] % len(st.session_state.days)]
    st.caption(f"Next simulation step is **{day_of_week}**")
    
    if st.button("Simulate 1 Day", use_container_width=True):
        simulate_one_day()
        st.toast(f"Simulated {day_of_week}. {len(st.session_state.last_sim_results)} client attempts made.")
    
    if st.button("Simulate 1 Week", use_container_width=True):
        simulate_n_days(len(st.session_state.days))
        st.toast("Simulated 5 days (1 Week cycle).")

with col_status_msg:
    st.subheader("Recent Simulation Results")
    if st.session_state.last_sim_results:
        results_df = pd.DataFrame(st.session_state.last_sim_results)
        st.dataframe(results_df, use_container_width=True, height=200)
    else:
        st.info("Run a simulation step to see the results here.")

st.write("---")

# --- 4. UTILIZATION INSIGHTS (NEW PLACEMENT) ---
st.subheader("4. Utilization Insights")
col_util, col_booked, col_rev_avg = st.columns(3)

left_only = sum(1 for v in st.session_state.schedule.values() if v["status"] == "free")
booked = st.session_state.metrics['current_week_hours']
total_slots = len(st.session_state.schedule)

fill_percent = (booked / total_slots) * 100 if total_slots > 0 else 0

col_util.metric(
    "Free Slots (Capacity Remaining)", 
    left_only, 
    delta=f"{100 - fill_percent:.1f}% Unused"
)
col_booked.metric(
    "Booked Slots", 
    booked, 
    delta=f"{fill_percent:.1f}% Utilized"
)
col_rev_avg.metric(
    "Average Revenue Per Booked Hour",
    f"R {st.session_state.metrics['total_revenue'] / booked:.2f}" if booked > 0 else "R 0.00"
)

st.write("---")

# --- 5. CLIENT LIST ---
st.subheader("5. Client Ledger")
clients_display = pd.DataFrame(st.session_state.clients).fillna("")
if clients_display.empty:
    st.write("No clients yet.")
else:
    expected_cols = ["id", "level", "rate", "weekly_hours", "active"]
    for col in expected_cols:
        if col not in clients_display.columns:
            clients_display[col] = None 

    clients_display = clients_display[expected_cols]
    st.dataframe(clients_display, use_container_width=True)

# --- FOOTER: EXPORT CONTROLS ---
st.write("---")
c1, c2 = st.columns([1,1])
with c1:
    df_export_data = schedule_to_dataframe().to_csv().encode('utf-8')
    st.download_button("Export Timetable CSV", df_export_data, "timetable.csv", "text/csv")
with c2:
    dfc_export_data = pd.DataFrame(st.session_state.clients).to_csv(index=False).encode('utf-8')
    st.download_button("Export Clients CSV", dfc_export_data, "clients.csv", "text/csv")

st.caption("Simulation notes: new clients are created probabilistically. Level 2 clients pay more and can replace Level 1 clients (if allowed). Tune acquisition and reschedule probabilities in the sidebar.")