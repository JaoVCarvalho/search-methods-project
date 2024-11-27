import heapq
import random

def manhattan_distance(state, goal):
    distance = 0
    for i in range(1, 9):  # Numbers 1 to 8
        x1, y1 = divmod(state.index(i), 3)
        x2, y2 = divmod(goal.index(i), 3)
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

# Possible moves
def get_neighbors(state):
    neighbors = []
    zero_index = state.index(0)
    x, y = divmod(zero_index, 3)

    # Define possible moves (up, down, left, right)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    directions = ['Up', 'Down', 'Left', 'Right']

    for (dx, dy), direction in zip(moves, directions):
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            neighbor = state[:]
            neighbor[zero_index], neighbor[nx * 3 + ny] = neighbor[nx * 3 + ny], neighbor[zero_index]
            neighbors.append((neighbor, direction))

    return neighbors

# A* algorithm
def a_star(initial, goal):
    frontier = []
    heapq.heappush(frontier, (0 + manhattan_distance(initial, goal), initial, [], ""))  # (priority, state, path, move)
    explored = set()

    while frontier:
        _, current, path, moves = heapq.heappop(frontier)
        if current == goal:
            return path, moves

        explored.add(tuple(current))
        for neighbor, direction in get_neighbors(current):
            if tuple(neighbor) not in explored:
                new_path = path + [neighbor]
                new_moves = moves + f"Move: {direction}\n"
                priority = len(new_path) + manhattan_distance(neighbor, goal)
                heapq.heappush(frontier, (priority, neighbor, new_path, new_moves))

    return None, None

# Generate random initial state and goal state
def generate_puzzle():
    state = list(range(9))
    random.shuffle(state)
    return state

# Print the puzzle
def print_puzzle(state):
    for i in range(0, 9, 3):
        print(state[i:i + 3])
    print()

# Main logic
initial_state = generate_puzzle()
goal_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]  # Goal: [1, 2, 3, 4, 5, 6, 7, 8, 0]

print("Initial State:")
print_puzzle(initial_state)
print("Goal State:")
print_puzzle(goal_state)

# Solve puzzle
solution, moves = a_star(initial_state, goal_state)

if solution:
    print("Solution found in", len(solution), "steps:")
    for idx, step in enumerate(solution):
        print(f"Step {idx + 1}:")
        if idx < len(solution) - 1:
            # Display the move taken to reach the next step
            print(f"{moves.split('\n')[idx]}")
        print_puzzle(step)
else:
    print("No solution found.")