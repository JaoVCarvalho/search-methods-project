import heapq
import service

goal_state = [[1, 2, 3],
              [8, 0, 4],
              [7, 6, 5]]

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
    heapq.heappush(frontier, (0 + manhattan_distance(initial, goal_flat), initial, []))
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

def run(initial_random_state):

    initial_state = initial_random_state

    print("Generated Initial State:")
    for line in initial_state:
        print(line)
    print()

    solution_path = a_star(initial_state, goal_state)

    if solution_path:
        print("Solution found!")
        print()
        for step, state in enumerate(solution_path):
            print(f"Step {step}:")
            for line in state:
                print(line)
            print()
        service.animate_solution(solution_path, "A*  Solution")
    else:
        print("No solution found.")
        print()