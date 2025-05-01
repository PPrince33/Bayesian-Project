import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# Load data
merged_map = pd.read_csv('merged_map.csv')

# Title
st.title("🇪🇸 Spain 2nd Half Pass Prediction – 2024 UEFA Euro Final")

# Dropdown for start box
start_box = st.selectbox("Select Start Box", sorted(merged_map['box_start'].unique()))

# Filter data for selected start box
filtered = merged_map[merged_map['box_start'] == start_box]

# Ensure all 24 box_end entries are present (fill missing ones with 0s)
all_boxes = pd.DataFrame({'box_end': range(1, 25)})
for col in ['probability_prior', 'probability_1', 'posterior_probability', 'probability_2']:
    filtered = pd.merge(all_boxes, filtered[['box_end', col]], on='box_end', how='left')
    filtered[col] = filtered[col].fillna(0)

# Set up pitch styling
pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')

# Create 4 subplots
fig, axes = plt.subplots(1, 4, figsize=(28, 7), constrained_layout=True)
fig.set_facecolor('white')

titles = ['Prior Probability', '1st Half', 'Posterior', '2nd Half']
cols = ['probability_prior', 'probability_1', 'posterior_probability', 'probability_2']

# Draw each subplot
for ax, title, col in zip(axes, titles, cols):
    pitch.draw(ax=ax)
    ax.set_title(f'{title}\n(Box {start_box} → others)', color='black', fontsize=14)

    # Draw the 6x4 grid using dotted lines
    for x in range(20, 120, 20):
        ax.axvline(x=x, color='black', linestyle=':', linewidth=1)
    for y in range(20, 80, 20):
        ax.axhline(y=y, color='black', linestyle=':', linewidth=1)

    for i, row in filtered.iterrows():
        box_end = int(row['box_end'])
        prob = row[col]

        # Calculate box center (convert box_end to grid coordinates)
        col_idx = (box_end - 1) // 4
        row_idx = (box_end - 1) % 4
        x = col_idx * 20 + 10
        y = row_idx * 20 + 10

        # Always display the value, even if 0
        pitch.scatter(x, y, ax=ax, s=1000 * prob if prob > 0 else 50,
                      color='red' if prob > 0 else 'lightgrey',
                      alpha=0.6, edgecolors='black', zorder=3)
        ax.text(x, y, f'{prob:.2f}', ha='center', va='center',
                color='black' if prob > 0 else 'grey', fontsize=8)

st.pyplot(fig)
