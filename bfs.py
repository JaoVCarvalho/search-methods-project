from collections import deque
import service

goal_state = [[1, 2, 3],
              [8, 0, 4],
              [7, 6, 5]]

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

def run(initial_random_state):

    initial_state = initial_random_state

    print("Generated Initial State:")
    for line in initial_state:
        print(line)
    print()

    solution_path = breadth_first_search(initial_state, goal_state)

    if solution_path:
        print("Solution found!")
        print()
        print_path(solution_path)
        service.animate_solution(solution_path, "BFS Solution")
    else:
        print("No solution found.")
        print()