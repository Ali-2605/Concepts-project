
from typing import List, Tuple, Optional, Dict


Board = List[List[int]]

def board_to_tuple(board: Board) -> Tuple:
    """Convert mutable board to immutable tuple for hashing."""
    rows_as_tuples = []
    for row in board:
        rows_as_tuples.append(tuple(row))
    return tuple(rows_as_tuples)


def tuple_to_board(board_tuple: Tuple) -> Board:
    """Convert immutable tuple back to mutable board."""
    board: Board = []
    for row in board_tuple:
        board.append(list(row))
    return board


def copy_board(board: Board) -> Board:
    """Create a deep copy of the board."""
    new_board: Board = []
    for row in board:
        new_board.append(row[:])
    return new_board


def find_zero(board: Board) -> Tuple[int, int]:
  
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 0:
                return (row, col)
    return (-1, -1)


def get_neighbors(board: Board) -> List[Board]:
  
    neighbors = []
    zero_row, zero_col = find_zero(board)
    

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in directions:
        new_row = zero_row + dr
        new_col = zero_col + dc
        
    
        if 0 <= new_row < 3 and 0 <= new_col < 3:
           
            new_board = copy_board(board)
            new_board[zero_row][zero_col], new_board[new_row][new_col] = \
                new_board[new_row][new_col], new_board[zero_row][zero_col]
            neighbors.append(new_board)
    
    return neighbors


def manhattan_distance(board: Board, goal: Board) -> int:
   
    distance = 0
    
    goal_pos = {}
    for row in range(3):
        for col in range(3):
            goal_pos[goal[row][col]] = (row, col)
    

    for row in range(3):
        for col in range(3):
            tile = board[row][col]
            if tile != 0:
                goal_row, goal_col = goal_pos[tile]
                distance += abs(row - goal_row) + abs(col - goal_col)
    
    return distance


def a_star_search(start: Board, goal: Board, max_iterations: int = 100000) -> Optional[List[Board]]:

    start_tuple = board_to_tuple(start)
    goal_tuple = board_to_tuple(goal)

    open_set = [(manhattan_distance(start, goal), 0, start_tuple, [copy_board(start)])]
    closed_set = set()
    g_score = {start_tuple: 0}
    counter = 1
    iterations = 0
    
    while open_set and iterations < max_iterations:
        iterations = iterations + 1
        
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
        

        neighbors = get_neighbors(current_board)
        for neighbor in neighbors:
            neighbor_tuple = board_to_tuple(neighbor)
            
            if neighbor_tuple in closed_set:
                continue
            
            tentative_g = current_g + 1

            if neighbor_tuple not in g_score or tentative_g < g_score[neighbor_tuple]:
                g_score[neighbor_tuple] = tentative_g
                h_score = manhattan_distance(neighbor, goal)
                f = tentative_g + h_score
                
                path_copy = []
                for b in path:
                    path_copy.append(copy_board(b))
                path_copy.append(copy_board(neighbor))
                

                open_set.append((f, counter, neighbor_tuple, path_copy))
                counter = counter + 1
    
    return None


def print_board(board: Board) -> None:
    """
    Display the board in a readable format using imperative loops.
    """
    print("+-------+")
    
    for row in board:
        print("|", end="")
        for tile in row:
            if tile == 0:
                print("   ", end="")
            else:
                print(f" {tile} ", end="")
        print("|")
    
    print("+-------+")
    print()


def main():

    initial_board = [
        [8, 6, 7],
        [2, 5, 4],
        [3, 0, 1]
    ]
    

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
