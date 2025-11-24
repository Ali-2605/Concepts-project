"""
Sliding 8-Puzzle - Imperative Programming Version

This module implements the 8-puzzle using classic imperative programming:
- Mutable data structures (list of lists for board representation)
- Iterative algorithms using loops instead of recursion
- Explicit state management and control flow
- Straightforward step-by-step problem solving

The board is represented as a list of lists, where 0 represents the empty space.
Example board:
[[1, 2, 3],
 [4, 0, 5], 
 [7, 8, 6]]
"""

from typing import List, Tuple, Optional, Dict

# Type alias for mutable board representation
Board = List[List[int]]

def board_to_tuple(board: Board) -> Tuple:
    """Convert mutable board to immutable tuple for hashing."""
    return tuple(tuple(row) for row in board)


def tuple_to_board(board_tuple: Tuple) -> Board:
    """Convert immutable tuple back to mutable board."""
    return [list(row) for row in board_tuple]


def copy_board(board: Board) -> Board:
    """Create a deep copy of the board."""
    return [row[:] for row in board]


def find_zero(board: Board) -> Tuple[int, int]:
    """Find the position of the empty tile (0)."""
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 0:
                return (row, col)
    return (-1, -1)


def get_neighbors(board: Board) -> List[Board]:
    """Generate all valid neighboring board states."""
    neighbors = []
    zero_row, zero_col = find_zero(board)
    
    # Define the four possible directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in directions:
        new_row = zero_row + dr
        new_col = zero_col + dc
        
        # Check if the new position is within bounds
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            # Create a copy and swap
            new_board = copy_board(board)
            new_board[zero_row][zero_col], new_board[new_row][new_col] = \
                new_board[new_row][new_col], new_board[zero_row][zero_col]
            neighbors.append(new_board)
    
    return neighbors


def manhattan_distance(board: Board, goal: Board) -> int:
    """Calculate the Manhattan distance heuristic."""
    distance = 0
    
    # Create a goal position map for quick lookup
    goal_pos = {}
    for row in range(3):
        for col in range(3):
            goal_pos[goal[row][col]] = (row, col)
    
    # Calculate distance for each tile
    for row in range(3):
        for col in range(3):
            tile = board[row][col]
            if tile != 0:  # Skip the empty space
                goal_row, goal_col = goal_pos[tile]
                distance += abs(row - goal_row) + abs(col - goal_col)
    
    return distance


def a_star_search(start: Board, goal: Board, max_iterations: int = 100000) -> Optional[List[Board]]:
    """
    Solve 8-puzzle using A* search algorithm (imperative approach).
    
    Uses explicit control flow with loops, mutable data structures,
    and state management typical of imperative programming.
    """
    start_tuple = board_to_tuple(start)
    goal_tuple = board_to_tuple(goal)
    
    # Priority queue represented as list (could use heapq for efficiency)
    # Each element: (f_score, counter, board_tuple, path)
    open_set = [(manhattan_distance(start, goal), 0, start_tuple, [copy_board(start)])]
    closed_set = set()
    g_score = {start_tuple: 0}
    counter = 1
    iterations = 0
    
    while open_set and iterations < max_iterations:
        iterations += 1
        
        # Find the node with the lowest f_score
        best_idx = 0
        for i in range(1, len(open_set)):
            if open_set[i][0] < open_set[best_idx][0]:
                best_idx = i
        
        f_score, _, current_tuple, path = open_set.pop(best_idx)
        current_board = tuple_to_board(current_tuple)
        
        if current_tuple == goal_tuple:
            return path
        
        closed_set.add(current_tuple)
        current_g = g_score[current_tuple]
        
        # Explore neighbors
        neighbors = get_neighbors(current_board)
        for neighbor in neighbors:
            neighbor_tuple = board_to_tuple(neighbor)
            
            if neighbor_tuple in closed_set:
                continue
            
            tentative_g = current_g + 1
            
            # Check if this is a better path
            if neighbor_tuple not in g_score or tentative_g < g_score[neighbor_tuple]:
                g_score[neighbor_tuple] = tentative_g
                h_score = manhattan_distance(neighbor, goal)
                f = tentative_g + h_score
                
                path_copy = [copy_board(b) for b in path]
                path_copy.append(copy_board(neighbor))
                
                # Add to open set
                open_set.append((f, counter, neighbor_tuple, path_copy))
                counter += 1
    
    return None


def print_board(board: Board) -> None:
    """
    Display the board in a readable format using imperative loops.
    """
    print("┌─────────┐")
    
    for row in board:
        print("│", end="")
        for tile in row:
            if tile == 0:
                print("   ", end="")
            else:
                print(f" {tile} ", end="")
        print("│")
    
    print("└─────────┘")
    print()


def main():
    """
    Main function demonstrating imperative approach to 8-puzzle solving.
    
    Shows explicit control flow, state management, and iterative algorithms
    typical of imperative programming paradigm.
    """
    # Create initial board state using mutable data structures
    initial_board = [
        [8, 6, 7],
        [2, 5, 4],
        [3, 0, 1]
    ]
    
    # Define goal state
    goal_board = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    print("=== Imperative 8-Puzzle Solver ===")
    print("\nInitial Board:")
    print_board(initial_board)
    
    print("Goal Board:")
    print_board(goal_board)
    
    print("Solving using A* search...\n")
    
    # Solve using imperative A* search
    solution = a_star_search(initial_board, goal_board)
    
    if solution:
        print(f"Solution found in {len(solution) - 1} moves:\n")
        
        for i, board_state in enumerate(solution):
            print(f"Step {i}:")
            print_board(board_state)
    else:
        print("No solution found within iteration limit.")
    
    print("Initial board value (may be modified by reference):")
    print_board(initial_board)


if __name__ == "__main__":
    main()
