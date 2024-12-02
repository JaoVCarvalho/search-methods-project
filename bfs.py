import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import random
from matplotlib.animation import FuncAnimation

goal_state = [[1, 2, 3],
              [8, 0, 4],
              [7, 6, 5]]

def generate_random_state():
    flattened = list(range(9))
    random.shuffle(flattened)
    return [flattened[i:i + 3] for i in range(0, 9, 3)]

def find_zero(state):
    for row in range(len(state)):
        for col in range(len(state[row])):
            if state[row][col] == 0:
                return row, col

def generate_successors(state):
    row, col = find_zero(state)
    moves = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]  # up, down, left, right
    successors = []

    for new_row, new_col in moves:
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = [line[:] for line in state]
            new_state[row][col], new_state[new_row][new_col] = (
                new_state[new_row][new_col],
                new_state[row][col],
            )
            successors.append(new_state)
    return successors

def breadth_first_search(initial_state, goal_state):
    queue = deque([initial_state])
    visited = set()
    parents = {str(initial_state): None}

    while queue:
        current_state = queue.popleft()
        if current_state == goal_state:
            return reconstruct_path(current_state, parents)

        visited.add(str(current_state))

        for successor in generate_successors(current_state):
            if str(successor) not in visited:
                queue.append(successor)
                parents[str(successor)] = current_state

    return None

def reconstruct_path(final_state, parents):
    path = []
    state = final_state
    while state:
        path.append(state)
        state = parents.get(str(state))
    return path[::-1]

def print_path(path):
    for step, state in enumerate(path):
        print(f"Step {step}:")
        for line in state:
            print(line)
        print()

def plot_state(state, ax):
    ax.clear()
    ax.set_xticks(np.arange(4) - 0.5, minor=True)
    ax.set_yticks(np.arange(4) - 0.5, minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=2)
    ax.set_xticks([])
    ax.set_yticks([])

    # Inverter a matriz para corrigir a orientação
    flipped_state = state[::-1]

    for i in range(3):
        for j in range(3):
            tile_value = flipped_state[i][j]
            ax.text(j, i, str(tile_value), ha='center', va='center', fontsize=20,
                    color='white' if tile_value != 0 else 'black',
                    bbox=dict(facecolor='blue' if tile_value != 0 else 'white',
                              edgecolor='black', boxstyle='round,pad=1'))


def animate_solution(solution_path):
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.suptitle("8 Puzzle", fontsize=16)

    def update(frame):
        plot_state(solution_path[frame], ax)
        ax.set_title(f"Step {frame}")

    anim = FuncAnimation(fig, update, frames=len(solution_path), interval=1000, repeat=False)
    plt.show()

def run():
    while True:
        user_input = input("Press Enter to generate a new initial state, or type 'q' to quit: ").strip()
        if user_input.lower() == "q":
            print("Exiting...")
            break

        initial_state = generate_random_state()
        print()
        print("Generated Initial State:")
        for line in initial_state:
            print(line)
        print()

        solution_path = breadth_first_search(initial_state, goal_state)

        if solution_path:
            print("Solution found!")
            print_path(solution_path)
            animate_solution(solution_path)
        else:
            print("No solution found.")

if __name__ == "__main__":
    run()
