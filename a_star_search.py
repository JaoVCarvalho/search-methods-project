import heapq
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

goal_state = [[1, 2, 3],
              [8, 0, 4],
              [7, 6, 5]]

def generate_random_state():
    flattened = list(range(9))
    random.shuffle(flattened)
    return [flattened[i:i + 3] for i in range(0, 9, 3)]

def manhattan_distance(state, goal):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                goal_row, goal_col = divmod(goal.index(value), 3)
                distance += abs(i - goal_row) + abs(j - goal_col)
    return distance

def get_neighbors(state):
    neighbors = []
    zero_row, zero_col = next((i, j) for i in range(3) for j in range(3) if state[i][j] == 0)

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in moves:
        new_row, new_col = zero_row + dx, zero_col + dy
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = [row[:] for row in state]
            new_state[zero_row][zero_col], new_state[new_row][new_col] = (
                new_state[new_row][new_col],
                new_state[zero_row][zero_col],
            )
            neighbors.append(new_state)
    return neighbors

def flatten_state(state):
    return [cell for row in state for cell in row]

def a_star(initial, goal):
    frontier = []
    goal_flat = flatten_state(goal)
    heapq.heappush(frontier, (0 + manhattan_distance(initial, goal_flat), initial, []))  # (priority, state, path)
    explored = set()

    while frontier:
        _, current, path = heapq.heappop(frontier)
        if current == goal:
            return path + [current]

        explored.add(tuple(flatten_state(current)))
        for neighbor in get_neighbors(current):
            flat_neighbor = tuple(flatten_state(neighbor))
            if flat_neighbor not in explored:
                priority = len(path) + manhattan_distance(neighbor, goal_flat)
                heapq.heappush(frontier, (priority, neighbor, path + [current]))

    return None

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

def animate_solution(solution_path):
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.suptitle("8 Puzzle - A* Solution", fontsize=16)

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
        print("\nGenerated Initial State:")
        for line in initial_state:
            print(line)
        print()

        solution_path = a_star(initial_state, goal_state)

        if solution_path:
            print("Solution found!")
            for step, state in enumerate(solution_path):
                print(f"Step {step}:")
                for line in state:
                    print(line)
                print()
            animate_solution(solution_path)
        else:
            print("No solution found.")

if __name__ == "__main__":
    run()
