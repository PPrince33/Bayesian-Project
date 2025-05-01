
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

# Set up pitch
pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#efefef')

# Create 4 subplots
fig, axes = plt.subplots(1, 4, figsize=(28, 7), constrained_layout=True)
fig.set_facecolor('#22312b')
titles = ['Prior Probability', '1st Half', 'Posterior', '2nd Half']
cols = ['probability_prior', 'probability_1', 'posterior_probability', 'probability_2']

for ax, title, col in zip(axes, titles, cols):
    pitch.draw(ax=ax)
    ax.set_title(f'{title}\n(Box {start_box} → others)', color='white', fontsize=14)

    for _, row in filtered.iterrows():
        box_end = int(row['box_end'])
        prob = row[col]

        if prob > 0:
            # Convert box_end (1 to 24) into grid coordinates
            col_idx = (box_end - 1) // 4
            row_idx = (box_end - 1) % 4
            x = col_idx * 20 + 10
            y = row_idx * 20 + 10

            pitch.scatter(x, y, ax=ax, s=1000 * prob, color='red', alpha=0.6, edgecolors='black', zorder=3)
            ax.text(x, y, f'{prob:.2f}', ha='center', va='center', color='white', fontsize=8)

st.pyplot(fig)
