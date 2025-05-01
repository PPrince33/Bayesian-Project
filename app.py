import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# Load data
merged_map = pd.read_csv('merged_map.csv')

# Streamlit page title
st.title("🇪🇸 Spain 2nd Half Pass Prediction – 2024 UEFA Euro Final")

# Dropdown to select the start box
start_box = st.selectbox("Select Start Box", sorted(merged_map['box_start'].unique()))

# Filter data for selected start box
filtered = merged_map[merged_map['box_start'] == start_box]

# Ensure all 24 destination boxes exist (for 0 probability display)
all_boxes = pd.DataFrame({'box_end': range(1, 25)})
for col in ['probability_prior', 'probability_1', 'posterior_probability', 'probability_2']:
    filtered = pd.merge(all_boxes, filtered[['box_end', col]], on='box_end', how='left')
    filtered[col] = filtered[col].fillna(0)

# Function to draw one pitch
def draw_single_pitch(prob_col, title):
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
    fig, ax = pitch.draw(figsize=(12, 8))
    fig.set_facecolor('white')
    ax.set_title(f"{title} (Start Box {start_box})", fontsize=16, color='black')

    # Draw dotted grid (vertical every 20m, horizontal every 20m)
    for x in range(20, 120, 20):
        ax.axvline(x=x, color='black', linestyle=':', linewidth=1)
    for y in range(20, 80, 20):
        ax.axhline(y=y, color='black', linestyle=':', linewidth=1)

    # Plot pass probabilities from selected box
    for _, row in filtered.iterrows():
        box_end = int(row['box_end'])
        prob = row[prob_col]

        # Convert box_end to correct x,y center
        col_idx = (box_end - 1) // 4  # vertical strips left to right
        row_idx = (box_end - 1) % 4   # rows from bottom to top

        x = col_idx * 20 + 10
        y = row_idx * 20 + 10

        pitch.scatter(x, y, ax=ax,
                      s=1000 * prob if prob > 0 else 50,
                      color='red' if prob > 0 else 'lightgrey',
                      alpha=0.6, edgecolors='black', zorder=3)
        ax.text(x, y, f'{prob:.2f}', ha='center', va='center',
                color='black' if prob > 0 else 'grey', fontsize=9)

    return fig

# Render 4 pitch visualizations stacked vertically
pitch_titles = ['Prior Probability', '1st Half', 'Posterior', '2nd Half']
pitch_cols = ['probability_prior', 'probability_1', 'posterior_probability', 'probability_2']

for title, col in zip(pitch_titles, pitch_cols):
    st.pyplot(draw_single_pitch(col, title))
