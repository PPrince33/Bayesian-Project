# Function to draw a single pitch visualization (with box numbers)
def draw_single_pitch(prob_col, title):
    data = filtered_maps[prob_col]

    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
    fig, ax = pitch.draw(figsize=(12, 8))
    fig.set_facecolor('white')
    ax.set_title(f"{title} (From Box {start_box})", fontsize=16, color='black')

    # Dotted gridlines
    for x in range(20, 120, 20):
        ax.axvline(x=x, color='black', linestyle=':', linewidth=1)
    for y in range(20, 80, 20):
        ax.axhline(y=y, color='black', linestyle=':', linewidth=1)

    # 📦 Draw box numbers (1–24) at center of each box
    for box_num in range(1, 25):
        col_idx = (box_num - 1) // 4
        row_idx = (box_num - 1) % 4
        x = col_idx * 20 + 10
        y = row_idx * 20 + 10
        ax.text(x, y + 7, str(box_num), ha='center', va='center', fontsize=10, color='grey', alpha=0.5)

    # 🔴 Draw probability dots + labels
    for _, row in data.iterrows():
        box_end = int(row['box_end'])
        prob = row[prob_col]

        col_idx = (box_end - 1) // 4
        row_idx = (box_end - 1) % 4
        x = col_idx * 20 + 10
        y = row_idx * 20 + 10

        pitch.scatter(x, y, ax=ax,
                      s=20000 * prob if prob > 0 else 50,
                      color='red' if prob > 0 else 'white',
                      alpha=0.6, edgecolors='white', zorder=3)

        ax.text(x, y, f'{prob:.2f}', ha='center', va='center',
                color='black' if prob > 0 else 'grey', fontsize=9)

    return fig
