import random


GOAL_BOARD = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]


def print_board(board):
    for row in board:
        print(" ".join(map(str, row)))


def get_blank_position(board):
    for r in range(3):
        for c in range(3):
            if board[r][c] == 0:
                return r, c
    return -1, -1


def apply_move(board, move_delta):
    """
    Applies a move (dr, dc) to the board.
    Returns the new board or None if the move is invalid.
    move_delta is a tuple (dr, dc)
    """
    br, bc = get_blank_position(board)
    new_board = [row[:] for row in board]  # Deep copy

    dr, dc = move_delta
    target_r, target_c = br + dr, bc + dc

    if 0 <= target_r < 3 and 0 <= target_c < 3:
        new_board[br][bc], new_board[target_r][target_c] = \
            new_board[target_r][target_c], new_board[br][bc]
        return new_board
    return None  # Move is out of bounds


def get_manhattan_distance(board):
    """
    Calculates the Manhattan distance heuristic for a given board from the GOAL_BOARD.
    """
    distance = 0
    for r_current in range(3):
        for c_current in range(3):
            tile = board[r_current][c_current]
            if tile == 0:
                continue  # Ignore blank tile

            # Calculate target row and column for the tile
            # Assuming target is 1-8 in order, then 0 at (2,2)
            r_target, c_target = 0, 0
            if tile == 1:
                r_target, c_target = 0, 0
            elif tile == 2:
                r_target, c_target = 0, 1
            elif tile == 3:
                r_target, c_target = 0, 2
            elif tile == 4:
                r_target, c_target = 1, 0
            elif tile == 5:
                r_target, c_target = 1, 1
            elif tile == 6:
                r_target, c_target = 1, 2
            elif tile == 7:
                r_target, c_target = 2, 0
            elif tile == 8:
                r_target, c_target = 2, 1

            distance += abs(r_current - r_target) + abs(c_current - c_target)
    return distance


def get_neighbors(board):
    """
    Generates all possible next board configurations by sliding the blank tile.
    Returns a list of (new_board, move_description) tuples.
    """
    neighbors = []
    br, bc = get_blank_position(board)

    # Possible moves: (dr, dc)
    moves_map = {
        (-1, 0): "Up",
        (1, 0): "Down",
        (0, -1): "Left",
        (0, 1): "Right"
    }

    for dr, dc in moves_map:
        new_board = apply_move(board, (dr, dc))
        if new_board:
            neighbors.append((new_board, moves_map[(dr, dc)]))
    return neighbors


def is_solvable(board):
    """
    Checks if an 8-puzzle configuration is solvable.
    (Same as in A* solver)
    """
    flat_board = []
    for row in board:
        for tile in row:
            if tile != 0:
                flat_board.append(tile)

    inversions = 0
    n = len(flat_board)
    for i in range(n):
        for j in range(i + 1, n):
            if flat_board[i] > flat_board[j]:
                inversions += 1

    return inversions % 2 == 0


# --- Stochastic Hill Climbing Solver ---

def solve_8_puzzle_stochastic_hill_climbing(initial_board, max_iterations=100000, max_restarts=10):
    if not is_solvable(initial_board):
        print("The initial puzzle configuration is not solvable.")
        return None

    best_overall_board = None
    min_overall_cost = float('inf')
    best_overall_path = []

    for restart_attempt in range(max_restarts):
        print(f"\nRestart Attempt {restart_attempt + 1}/{max_restarts}")
        current_board = [row[:] for row in initial_board]
        current_cost = get_manhattan_distance(current_board)
        current_path = [(initial_board, "Initial State")]

        print(f"Initial Cost for this attempt: {current_cost}")

        for iteration in range(max_iterations):
            if current_cost == 0:
                print(f"Solution found in {iteration} iterations!")
                if current_cost < min_overall_cost:
                    best_overall_board = current_board
                    min_overall_cost = current_cost
                    best_overall_path = current_path
                return best_overall_path  # Return the path if a solution is found

            neighbors = get_neighbors(current_board)

            # Filter for neighbors that improve the cost
            improving_neighbors = []
            for neighbor_board, move_desc in neighbors:
                neighbor_cost = get_manhattan_distance(neighbor_board)
                if neighbor_cost < current_cost:
                    improving_neighbors.append((neighbor_board, move_desc, neighbor_cost))

            if improving_neighbors:
                # Choose a random neighbor from the improving ones
                chosen_neighbor_board, chosen_move_desc, chosen_cost = random.choice(improving_neighbors)

                current_board = chosen_neighbor_board
                current_cost = chosen_cost
                current_path.append((current_board, chosen_move_desc))
            else:
                # No strictly improving neighbors found (stuck in local optimum or plateau)
                # Option 1: Break and restart (this is handled by the outer loop)
                # Option 2: Random walk (take a random move, even if it doesn't improve)
                # This implementation breaks and relies on restarts for global search.
                # To implement a random walk, you'd choose a random neighbor from ALL neighbors here.
                break  # Stuck in local optimum, break current climb and restart

            if iteration % 10000 == 0:
                print(f"  Iteration {iteration}: Current Cost = {current_cost}")

        # After an attempt, check if we found a better overall state
        if current_cost < min_overall_cost:
            best_overall_board = current_board
            min_overall_cost = current_cost
            best_overall_path = current_path

        print(f"Attempt finished with cost: {current_cost}")

    print(f"\nMax restarts ({max_restarts}) reached. Best board found overall:")
    if best_overall_board:
        print_board(best_overall_board)
        print(f"Final Manhattan distance: {min_overall_cost}")
        return best_overall_path
    else:
        print("Could not find any solution.")
        return None


def print_solution_path(path):
    if not path:
        print("No solution path to display.")
        return

    print("\nSolution Path (Stochastic Hill Climbing):")
    for i, (board, action) in enumerate(path):
        print(f"\nStep {i}: {action}")
        print_board(board)


# --- Main Execution ---
if __name__ == "__main__":
    # Example initial puzzle configurations

    # Solvable example (relatively easy for SHC)
    initial_puzzle_easy = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 0, 8]
    ]

    # A slightly harder solvable example
    initial_puzzle_medium = [
        [1, 2, 3],
        [0, 4, 6],
        [7, 5, 8]
    ]

    # A harder solvable example
    initial_puzzle_hard = [
        [2, 8, 3],
        [1, 6, 4],
        [7, 0, 5]
    ]

    # Unsolvable example (has an odd number of inversions)
    initial_puzzle_unsolvable = [
        [1, 2, 3],
        [4, 5, 6],
        [8, 7, 0]  # 8 and 7 are inverted
    ]

    print("Solving Easy Puzzle:")
    print("Initial Board:")
    print_board(initial_puzzle_easy)
    print("\nGoal Board:")
    print_board(GOAL_BOARD)
    print("-" * 30)

    solution_path_easy = solve_8_puzzle_stochastic_hill_climbing(initial_puzzle_easy, max_iterations=5000,
                                                                 max_restarts=5)
    print_solution_path(solution_path_easy)

    print("\n" + "=" * 30 + "\n")

    print("Solving Medium Puzzle:")
    print("Initial Board:")
    print_board(initial_puzzle_medium)
    print("\nGoal Board:")
    print_board(GOAL_BOARD)
    print("-" * 30)

    solution_path_medium = solve_8_puzzle_stochastic_hill_climbing(initial_puzzle_medium, max_iterations=50000,
                                                                   max_restarts=10)
    print_solution_path(solution_path_medium)

    print("\n" + "=" * 30 + "\n")

    print("Solving Hard Puzzle:")
    print("Initial Board:")
    print_board(initial_puzzle_hard)
    print("\nGoal Board:")
    print_board(GOAL_BOARD)
    print("-" * 30)

    # Stochastic Hill Climbing with restarts might need many iterations/restarts for harder puzzles.
    # It's not guaranteed to find the optimal path or even a solution.
    solution_path_hard = solve_8_puzzle_stochastic_hill_climbing(initial_puzzle_hard, max_iterations=200000,
                                                                 max_restarts=20)
    print_solution_path(solution_path_hard)

    print("\n" + "=" * 30 + "\n")

    print("Solving Unsolvable Puzzle:")
    print("Initial Board:")
    print_board(initial_puzzle_unsolvable)
    print("\nGoal Board:")
    print_board(GOAL_BOARD)
    print("-" * 30)

    solution_path_unsolvable = solve_8_puzzle_stochastic_hill_climbing(initial_puzzle_unsolvable, max_iterations=1000,
                                                                       max_restarts=1)
    print_solution_path(solution_path_unsolvable)