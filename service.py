import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random

def plot_state(state, ax):
    ax.clear()
    ax.set_xticks(np.arange(4) - 0.5, minor=True)
    ax.set_yticks(np.arange(4) - 0.5, minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=2)
    ax.set_xticks([])
    ax.set_yticks([])
    flipped_state = state[::-1]

    for i in range(3):
        for j in range(3):
            tile_value = flipped_state[i][j]
            ax.text(j, i, str(tile_value), ha='center', va='center', fontsize=20,
                    color='white' if tile_value != 0 else 'black',
                    bbox=dict(facecolor='blue' if tile_value != 0 else 'white',
                              edgecolor='black', boxstyle='round,pad=1'))

def animate_solution(solution_path, tittle):
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.suptitle(f"8 Puzzle - {tittle}", fontsize=16)

    def update(frame):
        plot_state(solution_path[frame], ax)
        ax.set_title(f"Step {frame}")

    anim = FuncAnimation(fig, update, frames=len(solution_path), interval=1000, repeat=False)
    plt.show()

def generate_random_state():
    flattened = list(range(9))
    random.shuffle(flattened)
    return [flattened[i:i + 3] for i in range(0, 9, 3)]

def print_default_bfs():
    print("================================")
    print("8 puzzles using BFS Solution")
    print("================================")
    print()

def print_default_a_star():
    print("===============================")
    print("8 puzzles using A* Solution")
    print("===============================")
    print()