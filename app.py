import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import seaborn as sns

# Load your CSV file (make sure it's in the same folder or adjust the path)
merged_map = pd.read_csv('merged_map.csv')

# Streamlit app title
st.title("🇪🇸 Spain 2nd Half Pass Prediction – 2024 UEFA Euro Final")

# Dropdown to choose the starting box
start_box = st.selectbox("Select Start Box", sorted(merged_map['box_start'].unique()))

# Ensure all destination boxes (1–24) are included
all_boxes = pd.DataFrame({'box_end': range(1, 25)})

# Prepare probability maps for each scenario
filtered_maps = {}
for col in ['probability_prior', 'probability_1', 'posterior_probability', 'probability_2']:
    temp = merged_map[merged_map['box_start'] == start_box][['box_end', col]]
    temp = pd.merge(all_boxes, temp, on='box_end', how='left')
    temp[col] = temp[col].fillna(0)
    filtered_maps[col] = temp

# Function to draw a pitch for a specific probability type
def draw_single_pitch(prob_col, title):
    data = filtered_maps[prob_col]

    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
    fig, ax = pitch.draw(figsize=(12, 8))
    fig.set_facecolor('white')
    ax.set_title(f"{title} (From Box {start_box})", fontsize=16, color='black')

    # Dotted gridlines (20m spacing)
    for x in range(20, 120, 20):
        ax.axvline(x=x, color='black', linestyle=':', linewidth=1)
    for y in range(20, 80, 20):
        ax.axhline(y=y, color='black', linestyle=':', linewidth=1)

    # Draw box numbers (1–24) with StatsBomb system: (0,0) is at the top left
    for box_num in range(1, 25):
        col_idx = (box_num - 1) // 4  # horizontal position
        row_idx = (box_num - 1) % 4   # vertical position
        x = col_idx * 20 + 10
        y = 80 - (row_idx * 20 + 10)  # Flip y to match StatsBomb system

        ax.text(x, y + 7, str(box_num), ha='center', va='center', fontsize=20, color='black', alpha=1)

    # Draw probabilities
    for _, row in data.iterrows():
        box_end = int(row['box_end'])
        prob = row[prob_col]

        col_idx = (box_end - 1) // 4
        row_idx = (box_end - 1) % 4
        x = col_idx * 20 + 10
        y = 80 - (row_idx * 20 + 10)  # Flip y to match StatsBomb system

        pitch.scatter(x, y, ax=ax,
                      s=20000 * prob if prob > 0 else 50,
                      color='red' if prob > 0 else 'white',
                      alpha=0.6, edgecolors='white', zorder=3)

        ax.text(x, y, f'{prob:.2f}', ha='center', va='center',
                color='black' if prob > 0 else 'grey', fontsize=9)

    return fig

# Draw all four visualizations vertically
titles = ['Prior Probability', '1st Half', 'Posterior (Bayesian)', '2nd Half']
cols = ['probability_prior', 'probability_1', 'posterior_probability', 'probability_2']

for title, col in zip(titles, cols):
    st.pyplot(draw_single_pitch(col, title))




# Load your CSV file (make sure it's in the same folder or adjust the path)
merged_map_2 = pd.read_csv('merged_map.csv')

# Create pivot tables for each probability type
pivot_prior = merged_map_2.pivot(index='box_start', columns='box_end', values='probability_prior').fillna(0)
pivot_1st_half = merged_map_2.pivot(index='box_start', columns='box_end', values='probability_1').fillna(0)
pivot_posterior = merged_map_2.pivot(index='box_start', columns='box_end', values='posterior_probability').fillna(0)
pivot_2nd_half = merged_map_2.pivot(index='box_start', columns='box_end', values='probability_2').fillna(0)

# Streamlit app title
st.title("Transition Matrix Heat Maps for Probability Types")

# Function to plot heatmap
def plot_heatmap(matrix, title):
    plt.figure(figsize=(10, 10))
    sns.heatmap(matrix, annot=False, cmap="viridis", fmt=".2f", cbar=True)
    plt.title(title, fontsize=16)
    st.pyplot(plt)

# Plot all four heatmaps for each transition matrix
st.subheader("Prior Probability Transition Matrix")
plot_heatmap(pivot_prior, "Prior Probability Transition Matrix")

st.subheader("1st Half Probability Transition Matrix")
plot_heatmap(pivot_1st_half, "1st Half Probability Transition Matrix")

st.subheader("Posterior Probability Transition Matrix")
plot_heatmap(pivot_posterior, "Posterior Probability Transition Matrix")

st.subheader("2nd Half Probability Transition Matrix")
plot_heatmap(pivot_2nd_half, "2nd Half Probability Transition Matrix")

