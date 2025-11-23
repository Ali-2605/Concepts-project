from typing import Tuple, List, Set, Optional

Board = Tuple[
    Tuple[int, int, int],
    Tuple[int, int, int], 
    Tuple[int, int, int]
]


def find_tile_position(target_board: Board, tile: int) -> Tuple[int, int]:
    def search_rows(row_idx: int) -> Tuple[int, int]:
        if row_idx >= 3:
            return (-1, -1)
        
        def search_cols(col_idx: int) -> Tuple[int, int]:
            if col_idx >= 3:
                return search_rows(row_idx + 1)
            if target_board[row_idx][col_idx] == tile:
                return (row_idx, col_idx)
            return search_cols(col_idx + 1)
        
        return search_cols(0)
    return search_rows(0)


def calculate_tile_distance(board: Board, goal: Board, tile: int) -> int:
    if tile == 0:
        return 0
    
    curr_row, curr_col = find_tile_position(board, tile)
    goal_row, goal_col = find_tile_position(goal, tile)
    
    if curr_row == -1 or goal_row == -1:
        return 0
    
    return abs(curr_row - goal_row) + abs(curr_col - goal_col)


def manhattan_distance(board: Board, goal: Board) -> int:
    def sum_distances(tile: int) -> int:
        if tile > 8:
            return 0
        return calculate_tile_distance(board, goal, tile) + sum_distances(tile + 1)
    
    return sum_distances(1)


def find_zero(board: Board) -> Tuple[int, int]:
    def search_rows(row_idx: int) -> Tuple[int, int]:
        if row_idx >= 3:
            return (-1, -1)
        
        def search_cols(col_idx: int) -> Tuple[int, int]:
            if col_idx >= 3:
                return search_rows(row_idx + 1)
            if board[row_idx][col_idx] == 0:
                return (row_idx, col_idx)
            return search_cols(col_idx + 1)
        
        return search_cols(0)
    
    return search_rows(0)


def swap(board: Board, r1: int, c1: int, r2: int, c2: int) -> Board:
    def build_row(row_idx: int, original_row: Tuple[int, int, int]) -> Tuple[int, int, int]:
        def build_cell(col_idx: int) -> Tuple[int, int, int]:
            if col_idx >= 3:
                return ()
            
            if row_idx == r1 and col_idx == c1:
                value = board[r2][c2]
            elif row_idx == r2 and col_idx == c2:
                value = board[r1][c1]
            else:
                value = original_row[col_idx]
            
            return (value,) + build_cell(col_idx + 1)
        
        return build_cell(0)
    
    def build_board(row_idx: int) -> Board:
        if row_idx >= len(board):
            return ()
        
        new_row = build_row(row_idx, board[row_idx])
        return (new_row,) + build_board(row_idx + 1)
    
    return build_board(0)


def next_states(board: Board) -> List[Board]:
    zero_row, zero_col = find_zero(board)
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    
    def generate_moves(dir_idx: int) -> List[Board]:
        if dir_idx >= len(directions):
            return []
        
        dr, dc = directions[dir_idx]
        new_row, new_col = zero_row + dr, zero_col + dc
        
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_board = swap(board, zero_row, zero_col, new_row, new_col)
            return [new_board] + generate_moves(dir_idx + 1)
        else:
            return generate_moves(dir_idx + 1)
    
    return generate_moves(0)


def insert_move_by_heuristic(move: Board, sorted_moves: List[Board], goal: Board) -> List[Board]:
    if not sorted_moves:
        return [move]
    
    move_distance = manhattan_distance(move, goal)
    first_distance = manhattan_distance(sorted_moves[0], goal)
    
    if move_distance <= first_distance:
        return [move] + sorted_moves
    else:
        return [sorted_moves[0]] + insert_move_by_heuristic(move, sorted_moves[1:], goal)


def sort_moves_by_heuristic(moves: List[Board], goal: Board) -> List[Board]:
    def sort_moves(unsorted: List[Board], sorted_result: List[Board]) -> List[Board]:
        if not unsorted:
            return sorted_result
        
        return sort_moves(
            unsorted[1:],
            insert_move_by_heuristic(unsorted[0], sorted_result, goal)
        )
    
    return sort_moves(moves, [])


def is_move_promising(move: Board, goal: Board, current_distance: int) -> bool:
    next_distance = manhattan_distance(move, goal)
    return next_distance <= current_distance + 2


def solve(board: Board, goal: Board, path: List[Board] = None, max_depth: int = 40) -> Optional[List[Board]]:
    if path is None:
        path = [board]
    
    if len(path) > max_depth:
        return None
    
    if board == goal:
        return path
    
    current_distance = manhattan_distance(board, goal)
    
    if board in path[:-1]:
        return None
    
    if len(path) > 25 and current_distance > len(path) * 1.3:
        return None
    
    possible_moves = next_states(board)
    sorted_moves = sort_moves_by_heuristic(possible_moves, goal)
    
    for next_board in sorted_moves:
        if (next_board not in path and 
            is_move_promising(next_board, goal, current_distance)):
            
            result = solve(next_board, goal, path + [next_board], max_depth)
            if result:
                return result
    
    return None


def print_board(board: Board) -> None:
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
    initial_board: Board = (
        (8, 6, 7),
        (2, 5, 4),
        (3, 0, 1)
    )
    
    goal_board: Board = (
        (1, 2, 3),  
        (4, 5, 6),  
        (7, 8, 0)   
    )
    
    print("=== Functional 8-Puzzle Solver ===")
    print("\nInitial Board:")
    print_board(initial_board)
    
    print("Goal Board:")
    print_board(goal_board)
    
    print("Solving...\n")
    
    solution = solve(initial_board, goal_board)
    
    if solution:
        print(f"Solution found in {len(solution) - 1} moves:")
        
        for i, board_state in enumerate(solution):
            print(f"Step {i}:")
            print_board(board_state)
    else:
        print("No solution found.")
    
    print("Original board after solving (unchanged):")
    print_board(initial_board)
    
if __name__ == "__main__":
    main()
