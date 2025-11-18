import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# ---------------------------
# Session state initialization
# ---------------------------
if 'current_maze_index' not in st.session_state:
    st.session_state.current_maze_index = 0
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1

# ---------------------------
# 1. Maze Definitions
# ---------------------------
MAZE_CONFIGS = [
    {
        "name": "1",
        "grid": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ],
        "start": (1, 1),
        "goal": (9, 10),
    },
    {
        "name": "2",
        "grid": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ],
        "start": (1, 1),
        "goal": (9, 1),
    },
    {
        "name": "3",
        "grid": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ],
        "start": (1, 1),
        "goal": (9, 10),
    }
]

# ---------------------------
# 2. convert_grid_to_graph
# ---------------------------
def convert_grid_to_graph(grid, start_pos_grid, goal_pos_grid):
    R, C = len(grid), len(grid[0])
    G = nx.Graph()
    
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    pos = {} 
    node_id_to_grid_pos = {} 
    grid_pos_to_node_id = {} 
    node_counter = 0

    for r in range(R):
        for c in range(C):
            if grid[r][c] == 0: # If it's a path
                node_id = node_counter
                grid_pos = (r, c)
                
                G.add_node(node_id, grid_pos=grid_pos) 
                pos[node_id] = (c, -r) 
                node_id_to_grid_pos[node_id] = grid_pos
                grid_pos_to_node_id[grid_pos] = node_id
                node_counter += 1

    # Second pass to ensure all edges are added
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 0:
                node_id = grid_pos_to_node_id[(r, c)]
                for i in range(4):
                    nr, nc = r + dr[i], c + dc[i]
                    if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0:
                        neighbor_id = grid_pos_to_node_id.get((nr, nc))
                        if neighbor_id is not None:
                            G.add_edge(node_id, neighbor_id, weight=1) 

    # Convert start/goal grid positions to their corresponding node IDs
    try:
        START_NODE = grid_pos_to_node_id[start_pos_grid]
        GOAL_NODE = grid_pos_to_node_id[goal_pos_grid]
    except KeyError:
        st.error(f"Start {start_pos_grid} or Goal {goal_pos_grid} position is inside a wall (1) or out of bounds. Please check the maze configuration.")
        return nx.Graph(), None, None, {}, {}, {}, {}

    # Calculate heuristic (Manhattan distance from each node's grid position to the goal)
    goal_r, goal_c = goal_pos_grid
    heuristic_data = {}
    for node_id in G.nodes:
        r, c = G.nodes[node_id]['grid_pos']
        h_value = abs(goal_r - r) + abs(goal_c - c)
        G.nodes[node_id]['h'] = h_value 
        heuristic_data[node_id] = h_value 

    node_labels = {k: f"H:{v}" for k, v in heuristic_data.items()}

    return G, START_NODE, GOAL_NODE, node_labels, pos, heuristic_data, node_id_to_grid_pos

# ---------------------------
# 3. A* Search
# ---------------------------
def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def a_star_search(G, start, goal):
    if start is None or goal is None:
        return None, [], pd.DataFrame()
        
    g_score = {node: float('inf') for node in G.nodes}
    g_score[start] = 0
    
    f_score = {node: float('inf') for node in G.nodes}
    f_score[start] = g_score[start] + G.nodes[start]['h']
    
    came_from = {}
    open_set = [(f_score[start], start)] 
    
    history = []
    equation_history_df = pd.DataFrame(columns=['Step', 'Current Node', 'F(n) = G(n) + H(n)', 'G(n)', 'H(n)'])
    step_count = 0

    while open_set:
        open_set.sort()
        current_f, current_node = open_set.pop(0)

        step_count += 1
        
        current_open_nodes = [n for _, n in open_set]
        # Nodes that have been fully evaluated (i.e., were 'current' but are no longer in open_set)
        # For visualization, we approximate closed set by nodes with finite g_score, excluding current and open_set
        closed_candidate = [node for node in g_score if g_score[node] != float('inf')]
        current_closed_nodes = [node for node in closed_candidate if node != current_node and node not in current_open_nodes]

        history.append({
            'step': step_count,
            'current': current_node,
            'open_set': current_open_nodes,
            'closed_set': current_closed_nodes,
            'path': reconstruct_path(came_from, current_node),
            'g_score': g_score.copy(),
            'f_score': f_score.copy()
        })
        
        equation_history_df.loc[len(equation_history_df)] = [
            step_count,
            current_node,
            f"{g_score[current_node]:.1f} + {G.nodes[current_node]['h']:.1f} = {f_score[current_node]:.1f}",
            f"{g_score[current_node]:.1f}",
            f"{G.nodes[current_node]['h']:.1f}"
        ]

        if current_node == goal:
            final_path = reconstruct_path(came_from, current_node)
            step_count += 1
            # Final history step to show the path clearly
            history.append({
                'step': step_count,
                'current': goal,
                'open_set': [],
                'closed_set': current_closed_nodes + [current_node],
                'path': final_path,
                'g_score': g_score.copy(),
                'f_score': f_score.copy()
            })
            equation_history_df.loc[len(equation_history_df)] = [
                step_count,
                goal,
                f"{g_score[goal]:.1f} + {G.nodes[goal]['h']:.1f} = {f_score[goal]:.1f}",
                f"{g_score[goal]:.1f}",
                f"{G.nodes[goal]['h']:.1f}"
            ]
            return final_path, history, equation_history_df

        for neighbor in G.neighbors(current_node):
            weight = G[current_node][neighbor]['weight']
            tentative_g_score = g_score[current_node] + weight

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + G.nodes[neighbor]['h']

                found_in_open = False
                for i, (f, node) in enumerate(open_set):
                    if node == neighbor:
                        open_set[i] = (f_score[neighbor], neighbor)
                        found_in_open = True
                        break
                if not found_in_open:
                    open_set.append((f_score[neighbor], neighbor))

    return None, history, equation_history_df

# ---------------------------
# 4. Visualization Utilities
# ---------------------------
def draw_graph_a_star(G, pos, start, goal, node_labels, current=None, open_set=[], closed_set=[], final_path=[], g_scores={}, f_scores={}, step_title=""):
    fig, ax = plt.subplots(figsize=(12, 10)) 
    node_color = ['#A3E4D7' for node in G.nodes] 
    
    for i, node in enumerate(G.nodes):
        if node == start:
            node_color[i] = 'red'
        elif node == goal:
            node_color[i] = 'green'
        elif node == current:
            node_color[i] = '#FFC300' 
        elif node in final_path:
            node_color[i] = '#9B59B6'
        elif node in open_set:
            node_color[i] = '#5DADE2'
        elif node in closed_set:
            node_color[i] = '#D7DBDD'
            
    edge_colors = ['gray'] * len(G.edges)
    edge_widths = [1] * len(G.edges)
    
    if final_path:
        path_edges = list(zip(final_path, final_path[1:]))
        for i, edge in enumerate(G.edges()):
            if (edge[0], edge[1]) in path_edges or (edge[1], edge[0]) in path_edges:
                edge_colors[i] = '#9B59B6'
                edge_widths[i] = 3

    nx.draw_networkx_nodes(G, pos, node_color=node_color, node_size=800, edgecolors='black', linewidths=1.0, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths, ax=ax)
    
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8, font_weight='bold', font_color='black', ax=ax)
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, label_pos=0.3, ax=ax)
    
    # Adjusted position for scores (g, h, f)
    score_pos_offset = {k: [v[0], v[1] - 0.05] for k, v in pos.items()}
    score_labels = {}
    for node in G.nodes:
        if node in f_scores and f_scores[node] != float('inf'):
            g = f"{g_scores.get(node, 0):.1f}"
            h = f"{G.nodes[node]['h']:.1f}"
            f = f"{f_scores[node]:.1f}"
            score_labels[node] = f"G: {g}\nH: {h}\nF: {f}"

    nx.draw_networkx_labels(G, score_pos_offset, labels=score_labels, font_size=7, font_color='darkred', ax=ax)

    ax.set_title(step_title, fontsize=14)
    st.pyplot(fig)


def draw_grid_maze_with_scent(maze_grid, node_id_to_grid_pos, start_node_id, goal_node_id, 
                              path_so_far_node_ids=[], heuristic_data={}):
    R, C = len(maze_grid), len(maze_grid[0])
    fig, ax = plt.subplots(figsize=(C, R)) 
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-0.5, C - 0.5) 
    ax.set_ylim(R - 0.5, -0.5) 
    ax.axis('off')

    max_h = max(heuristic_data.values()) if heuristic_data else 1
    
    # Custom colormap for 'scent' (heuristic value)
    colors = ["#FFFACD", "#FFD700", "#FFA500", "#FF8C00"] # Light yellow to dark orange
    scent_cmap = LinearSegmentedColormap.from_list("scent_cmap", colors, N=max_h + 1)

    for r in range(R):
        for c in range(C):
            if maze_grid[r][c] == 0:
                node_id = None
                for nid, gpos in node_id_to_grid_pos.items():
                    if gpos == (r,c):
                        node_id = nid
                        break
                
                if node_id is not None and node_id in heuristic_data:
                    h_val = heuristic_data[node_id]
                    # Color based on heuristic: closer to goal (lower H) is brighter (more appealing 'scent')
                    color = scent_cmap(1 - (h_val / max_h)) 
                    ax.add_patch(plt.Rectangle((c - 0.5, r - 0.5), 1, 1, facecolor=color, edgecolor='none', zorder=0))
                else:
                    ax.add_patch(plt.Rectangle((c - 0.5, r - 0.5), 1, 1, facecolor='lightgray', edgecolor='none', zorder=0))

    for r in range(R):
        for c in range(C):
            if maze_grid[r][c] == 1:
                ax.add_patch(plt.Rectangle((c - 0.5, r - 0.5), 1, 1, facecolor='black', edgecolor='black', zorder=1))

    # Draw the path so far
    if len(path_so_far_node_ids) > 1:
        path_grid_coords = [node_id_to_grid_pos[nid] for nid in path_so_far_node_ids if nid in node_id_to_grid_pos]
        path_x = [c for r, c in path_grid_coords]
        path_y = [r for r, c in path_grid_coords]
        # Draw path line
        ax.plot(path_x, path_y, color='red', linewidth=3, marker='o', markersize=8, markerfacecolor='red', markeredgecolor='darkred', zorder=4)

    # Highlight the current position (the mouse)
    if path_so_far_node_ids and path_so_far_node_ids[-1] in node_id_to_grid_pos:
        current_node_id = path_so_far_node_ids[-1]
        current_r, current_c = node_id_to_grid_pos[current_node_id]
        ax.add_patch(plt.Rectangle((current_c - 0.4, current_r - 0.4), 0.8, 0.8, facecolor='red', edgecolor='darkred', lw=1.5, zorder=5))

    # Highlight the goal (the cheese)
    if goal_node_id is not None and goal_node_id in node_id_to_grid_pos:
        goal_r, goal_c = node_id_to_grid_pos[goal_node_id]
        ax.plot(goal_c, goal_r, marker='o', markersize=20, color='green', markeredgecolor='darkgreen', lw=2, zorder=5)
    
    ax.set_title("Maze Map: Mouse Progress & Scent", fontsize=14)
    st.pyplot(fig)

# ---------------------------
# 5. Maze Navigation & Step callbacks (FIXED - st.experimental_rerun -> st.rerun)
# ---------------------------
def next_maze():             
    if st.session_state.current_maze_index < len(MAZE_CONFIGS) - 1:    
        st.session_state.current_maze_index += 1            
        st.session_state.current_step = 1            
        st.rerun()

def prev_maze():
    if st.session_state.current_maze_index > 0:
        st.session_state.current_maze_index -= 1
        st.session_state.current_step = 1
        st.rerun() # FIXED: Use st.rerun()

def next_step():
    # Safe increment
    if 'history_len' in st.session_state:
        st.session_state.current_step = min(st.session_state.current_step + 1, st.session_state.history_len)

def prev_step():
    if 'history_len' in st.session_state:
        st.session_state.current_step = max(1, st.session_state.current_step - 1)

def rewind_step():
    st.session_state.current_step = 1

def fast_forward_step():
    if 'history_len' in st.session_state:
        st.session_state.current_step = st.session_state.history_len

# ---------------------------
# 6. Main app
# ---------------------------
def main():
    st.set_page_config(layout="wide", page_title="A* Search for Cheese Visualization")

    st.title("🐭 A* Search for Cheese Visualization")
    st.markdown("---")

    # Load current maze
    current_maze_config = MAZE_CONFIGS[st.session_state.current_maze_index]
    MAZE_GRID = current_maze_config["grid"]
    START_POS_GRID = current_maze_config["start"]
    GOAL_POS_GRID = current_maze_config["goal"]

    # Convert grid -> graph and heuristics
    G, START_NODE, GOAL_NODE, node_labels, pos, heuristic_data_full, node_id_to_grid_pos = \
        convert_grid_to_graph(MAZE_GRID, START_POS_GRID, GOAL_POS_GRID)

    # Run A*
    final_path, history, equation_df = a_star_search(G, START_NODE, GOAL_NODE)

    # history length guard
    max_steps = len(history)
    st.session_state.history_len = max(1, max_steps)

    # Clamp current_step into valid range
    if st.session_state.current_step > st.session_state.history_len:
        st.session_state.current_step = st.session_state.history_len
    if st.session_state.current_step < 1:
        st.session_state.current_step = 1

    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Controls")

        # # Maze selector dropdown (keeps in sync with current_maze_index)
        # selected_maze_name = st.selectbox(
        #     "Choose a Maze",
        #     options=[config["name"] for config in MAZE_CONFIGS],
        #     index=st.session_state.current_maze_index,
        #     key='maze_select_box'
        # )
        # # If user changes dropdown, update index and reset step
        # new_index = [config["name"] for config in MAZE_CONFIGS].index(selected_maze_name)
        # if new_index != st.session_state.current_maze_index:
        #     st.session_state.current_maze_index = new_index
        #     st.session_state.current_step = 1
        #     st.rerun() # FIXED: Changed from st.experimental_rerun()

        st.markdown("### Maze Navigation")
        col_prev_maze, col_next_maze = st.columns(2)
        with col_prev_maze:
            st.button("⬅️ Previous Maze", on_click=prev_maze, disabled=(st.session_state.current_maze_index == 0))
        with col_next_maze:
            st.button("Next Maze ➡️", on_click=next_maze, disabled=(st.session_state.current_maze_index == len(MAZE_CONFIGS) - 1))

        st.markdown("---")
        st.subheader("Step Navigator")

        col_prev, col_next = st.columns(2)
        with col_prev:
            st.button("⬅️ Previous Step", on_click=prev_step, disabled=(st.session_state.current_step <= 1))
        with col_next:
            st.button("Next Step ➡️", on_click=next_step, disabled=(st.session_state.current_step >= st.session_state.history_len))

        col_start, col_end = st.columns(2)
        with col_start:
            st.button("Rewind to Start ⏪", on_click=rewind_step)
        with col_end:
            st.button("Fast Forward to End ⏩", on_click=fast_forward_step)

        st.markdown(f"**Current Step:** {st.session_state.current_step} / {st.session_state.history_len}")

        # Display path info only if found
        if GOAL_NODE is not None and final_path:
             if st.session_state.current_step == st.session_state.history_len:
                 st.success("🎉 Goal Reached!")
             try:
                 st.markdown(f"**Final Path Cost (G):** {history[-1]['g_score'][GOAL_NODE]:.1f}")
                 st.markdown(f"**Path Length (Nodes):** {len(final_path)}")
             except Exception:
                 # Defensive: sometimes history may be empty if algo returned None
                 pass
        elif START_NODE is not None and GOAL_NODE is not None:
             st.error("❌ Path not found (Algorithm completed without reaching goal)")

        st.markdown("---")
        st.info(
            """
            **A* Graph Node Colors:**
            - **Red:** Start (Mouse)
            - **Green:** Goal (Cheese)
            - **Yellow:** Currently Expanding Node
            - **Blue:** Open Set (Nodes to evaluate)
            - **Light Gray:** Closed Set (Evaluated Nodes)
            - **Purple:** Final Path (shown when goal is reached)
            """
        )

    # Main visualization
    if not history:
        st.error("A* search failed to run. Please check the maze configuration for connectivity.")
        return

    # Retrieve current state safely
    current_state = history[st.session_state.current_step - 1]

    col_main_viz, col_equation_history = st.columns([3, 1])

    with col_main_viz:
        st.subheader(f"🧀 Maze Map: {current_maze_config['name']}")
        draw_grid_maze_with_scent(
            MAZE_GRID,
            node_id_to_grid_pos,
            START_NODE,
            GOAL_NODE,
            path_so_far_node_ids=current_state['path'],
            heuristic_data=heuristic_data_full
        )

        st.markdown("---")

        st.subheader("🗺️ A* Graph Visualization")
        draw_graph_a_star(
            G, pos, START_NODE, GOAL_NODE, node_labels,
            current=current_state['current'],
            open_set=current_state['open_set'],
            closed_set=current_state['closed_set'],
            # Show final path only on the last step
            final_path=current_state['path'] if st.session_state.current_step == st.session_state.history_len and GOAL_NODE == current_state['current'] else [],
            g_scores=current_state['g_score'],
            f_scores=current_state['f_score'],
            step_title=f"A* Search: Step {st.session_state.current_step}"
        )

    with col_equation_history:
        st.subheader("📊 A* Equation History")
        if st.session_state.current_step <= len(equation_df):
            current_eq_row = equation_df[equation_df['Step'] == st.session_state.current_step].iloc[0]

            st.markdown(
                f"""
                ### **Step: {current_eq_row['Step']}**
                **Evaluating Node:** **{current_eq_row['Current Node']}**
                
                $$ F(n) = G(n) + H(n) $$
                $$ F({current_eq_row['Current Node']}) = {current_eq_row['G(n)']} + {current_eq_row['H(n)']} = {current_eq_row['F(n) = G(n) + H(n)'].split('=')[-1].strip()} $$
                """
            )
            st.markdown("---")
            st.dataframe(
                equation_df,
                height=600,
                use_container_width=True,
                hide_index=True,
                column_order=('Step', 'Current Node', 'F(n) = G(n) + H(n)'),
            )
        else:
            st.warning("Equation data for this step is not available yet.")

if __name__ == "__main__":
    main()
