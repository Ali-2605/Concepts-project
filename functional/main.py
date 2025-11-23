"""
Functional 8-Puzzle Solver

Demonstrates functional programming principles:
- Immutable data structures (tuples)
- Pure functions (no side effects)
- Recursive algorithms
- No variable mutation

Board representation: tuple of tuples, 0 = empty space
"""

from typing import Tuple, List, Set, Optional
# Type alias for immutable board representation
# Tuple[] means "an immutable sequence" - once created, it cannot be changed
# Unlike lists [1,2,3] which can be modified after creation,
# tuples (1,2,3) are "immutable" - they cannot be changed once created.
# Immutable 3x3 board type: tuple of three rows, each row is three integers
Board = Tuple[
    Tuple[int, int, int],
    Tuple[int, int, int], 
    Tuple[int, int, int]
]

# This prevents accidental modifications and ensures pure functions.


def find_tile_position(target_board: Board, tile: int) -> Tuple[int, int]:
    """
    Find where a specific tile is located on the board.
    
    Args:
        target_board: Board to search in
        tile: Tile number to find
        
    Returns:
        Tuple[int, int]: Position (row, col) of the tile, or (-1, -1) if not found
    """
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
    """
    Calculate Manhattan distance for a specific tile.
    
    Manhattan distance is the sum of horizontal and vertical distances a tile
    needs to move to reach its goal position. It's called "Manhattan" distance
    because it's like measuring city blocks in Manhattan where you can only
    move horizontally or vertically (no diagonal moves).
    
    Example: If tile 5 is at position (0,1) but should be at (2,1):
    Distance = |0-2| + |1-1| = 2 + 0 = 2 moves needed
    
    Args:
        board: Current board state
        goal: Target board state where we want this tile to be
        tile: Which tile number to calculate distance for (1-8)
        
    Returns:
        int: Manhattan distance for this specific tile (0 means it's in correct position)
    """
    # Special case: empty space (0) doesn't count toward distance
    if tile == 0:
        return 0
    
    curr_row, curr_col = find_tile_position(board, tile)
    
    # Find where this tile should be in the goal configuration
    goal_row, goal_col = find_tile_position(goal, tile)
    
    # Safety check: if tile wasn't found in either board, distance is 0
    if curr_row == -1 or goal_row == -1:
        return 0
    
    return abs(curr_row - goal_row) + abs(curr_col - goal_col)


def manhattan_distance(board: Board, goal: Board) -> int:
    """
    Calculate total Manhattan distance heuristic for the entire board.
    
    This is our "smart guess" about how far we are from solving the puzzle.
    It adds up the Manhattan distances for all tiles (1-8, skipping empty space).
    
    Why this matters: Instead of trying moves randomly, we can use this number
    to prioritize moves that seem to get us closer to the solution.
    
    Manhattan distance = sum of |current_row - goal_row| + |current_col - goal_col|
    for each numbered tile.
    
    Example board analysis:
    Current: [1,2,3]  Goal: [1,2,3]
             [0,4,6]       [4,5,6]  
             [7,5,8]       [7,8,0]
    
    Tile 4: at (1,1), should be at (1,0) → distance = 1
    Tile 5: at (2,1), should be at (1,1) → distance = 1  
    Tile 8: at (2,2), should be at (2,1) → distance = 1
    Total distance = 3 (minimum moves needed, though actual solution might need more)
    
    Args:
        board: Current board state
        goal: Target goal state
        
    Returns:
        int: Total heuristic distance (lower = closer to goal, 0 = solved)
    """
    # Inner recursive function to sum up distances for all tiles
    def sum_distances(tile: int) -> int:
        # Base case: we've processed all tiles (1 through 8)
        if tile > 8:
            return 0
        
        # Recursive case: distance for current tile + distances for remaining tiles
        # This adds up: distance(tile) + distance(tile+1) + ... + distance(8)
        return calculate_tile_distance(board, goal, tile) + sum_distances(tile + 1)
    
    # Start calculating from tile 1 (skip tile 0 which is the empty space)
    return sum_distances(1)


def find_zero(board: Board) -> Tuple[int, int]:
    """
    Find the position of the empty space (0) using pure recursion.
    
    FUNCTIONAL PROGRAMMING SHOWCASE:
    - Uses recursive functions instead of for/while loops
    - No mutable variables that change during execution
    - Pure function: same input always produces same output
    - No side effects: doesn't modify anything outside the function
    
    Args:
        board: The current board state (immutable tuple structure)
        
    Returns:
        Tuple[int, int]: The (row, column) position of the zero
        Example: (1, 1) means zero is at row 1, column 1
    """
    
    # NESTED FUNCTION PATTERN in functional programming
    # Instead of using nested loops, we use nested recursive functions
    # This demonstrates "function composition" - building complex behavior from simple functions
    def search_rows(row_idx: int) -> Tuple[int, int]:
        """
        Recursively search through each row of the board.
        
        RECURSION EXPLANATION:
        - Base case: if row_idx >= len(board), we've checked all rows
        - Recursive case: check current row, then move to next row
        
        Args:
            row_idx: Which row we're currently examining (0, 1, or 2)
        """
        
        # BASE CASE: Stop recursion when we've checked all rows
        if row_idx >= 3:  # 3 for our 3x3 board
            return (-1, -1)  # Return "not found" coordinates
        
        # INNER RECURSIVE FUNCTION for searching columns within this row
        def search_cols(col_idx: int) -> Tuple[int, int]:
            """
            Recursively search through each column in the current row.
            
            FUNCTIONAL PATTERN: Tail recursion
            - Each recursive call is the last operation in the function
            - No mutations or assignments to variables
            """
            
            # BASE CASE 1: Finished checking all columns in this row
            if col_idx >= 3:  # 3 for our 3x3 board
                # RECURSIVE CALL: Move to next row
                return search_rows(row_idx + 1)

            # BASE CASE 2: Found the zero!
            if board[row_idx][col_idx] == 0:
                # SUCCESS: Return the coordinates where we found zero
                return (row_idx, col_idx)

            # RECURSIVE CASE: Check next column in same row
            return search_cols(col_idx + 1)
        
        # Start searching columns from index 0
        return search_cols(0)
    
    # Start the entire search from row 0
    # FUNCTIONAL PRINCIPLE: Clear entry point with explicit parameters
    return search_rows(0)


def swap(board: Board, r1: int, c1: int, r2: int, c2: int) -> Board:
    """
    Create a completely new board with two positions swapped.
    
    This is a core functional programming principle: instead of modifying the original
    board (which would be a "side effect"), we create a brand new board with the
    desired changes. This ensures the original board remains unchanged.
    
    How it works: We recursively build a new 3x3 board, tile by tile. For each
    position, we decide what value it should have:
    - If it's position (r1,c1), use the value from position (r2,c2)
    - If it's position (r2,c2), use the value from position (r1,c1)
    - Otherwise, keep the original value
    
    Example: swap(board, 1, 1, 2, 2) swaps the values at (1,1) and (2,2)
    
    Args:
        board: Original board (will NOT be modified - immutability principle)
        r1, c1: First position coordinates (row, column) to swap
        r2, c2: Second position coordinates (row, column) to swap
        
    Returns:
        Board: Completely new board with the two positions swapped
    """
    # Function to build one row of the new board
    def build_row(row_idx: int, original_row: Tuple[int, int, int]) -> Tuple[int, int, int]:
        # Function to build each cell in this row
        def build_cell(col_idx: int) -> Tuple[int, int, int]:
            # Base case: finished building all 3 columns in this row
            if col_idx >= 3:
                return ()  # Empty tuple means "no more cells"
            
            # Determine what value this cell should have after the swap
            if row_idx == r1 and col_idx == c1:
                # This is the first swap position - give it the value from second position
                value = board[r2][c2]
            elif row_idx == r2 and col_idx == c2:
                # This is the second swap position - give it the value from first position
                value = board[r1][c1]
            else:
                # This position is not involved in the swap - keep original value
                value = original_row[col_idx]
            
            # Build the tuple: current cell + recursively build remaining cells
            # The comma after 'value' creates a single-element tuple
            return (value,) + build_cell(col_idx + 1)
        
        # Start building this row from column 0
        return build_cell(0)
    
    # Function to build the entire new board
    def build_board(row_idx: int) -> Board:
        # Base case: finished building all 3 rows
        if row_idx >= len(board):
            return ()  # Empty tuple means "no more rows"
        
        # Build current row using the row-building function above
        new_row = build_row(row_idx, board[row_idx])
        
        # Build the board: current row + recursively build remaining rows
        return (new_row,) + build_board(row_idx + 1)
    
    # Start building the entire board from row 0
    return build_board(0)


def next_states(board: Board) -> List[Board]:
    """
    Generate all possible next board states using pure recursion.
    
    FUNCTIONAL PROGRAMMING SHOWCASE:
    - Uses recursion instead of for loops
    - Creates new board states without modifying originals
    - Pure function with no side effects
    - Immutable direction data (tuple instead of list)
    
    This function finds where the empty space (0) can move and creates
    new board states for each valid move.
    
    Args:
        board: Current board state
        
    Returns:
        List[Board]: All possible board states reachable in one move
        Typically 2-4 states depending on where the empty space is located
    """
    
    # FUNCTIONAL PRINCIPLE: Use pure functions to gather information
    zero_row, zero_col = find_zero(board)
    
    # Move directions: up, down, left, right
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    
    def generate_moves(dir_idx: int) -> List[Board]:
        """
        Recursively try each possible move direction.
        
        FUNCTIONAL RECURSION PATTERN:
        - Base case: when all directions tried, return empty list
        - Recursive case: try current direction + recursively try remaining directions
        
        Args:
            dir_idx: Index of which direction we're currently trying (0, 1, 2, or 3)
            
        Returns:
            List of valid board states from this direction onward
        """
        
        # BASE CASE: Tried all directions
        if dir_idx >= len(directions):  # len(directions) = 4
            return []  # No more moves to try, return empty list
        
        # GET CURRENT DIRECTION: Extract the row and column changes
        dr, dc = directions[dir_idx]  # Tuple unpacking: dr=row_change, dc=col_change
        
        # CALCULATE NEW POSITION: Where the empty space would move to
        new_row, new_col = zero_row + dr, zero_col + dc
        
        # BOUNDS CHECKING: Make sure the new position is valid on our 3x3 board
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            # VALID MOVE: Create new board state with this move
            new_board = swap(board, zero_row, zero_col, new_row, new_col)
            
            # LIST CONCATENATION PATTERN: [current] + recursive_result
            # This builds the final list functionally without mutations
            # [new_board] creates a single-element list
            # + concatenates with list from recursive call
            return [new_board] + generate_moves(dir_idx + 1)
        else:
            # INVALID MOVE: Skip this direction and try remaining directions
            # TAIL RECURSION: Direct recursive call without adding anything
            return generate_moves(dir_idx + 1)
    
    # Start trying moves from direction index 0
    return generate_moves(0)


def insert_move_by_heuristic(move: Board, sorted_moves: List[Board], goal: Board) -> List[Board]:
    """
    Insert a board state into the correct position in a sorted list based on Manhattan distance.
    
    This is like insertion sort, but instead of sorting numbers, we're sorting board states
    by how "good" they are (measured by Manhattan distance to goal).
    
    The goal is to keep moves sorted from best (lowest distance) to worst (highest distance),
    so when we try moves later, we try the most promising ones first.
    
    How it works:
    - If the list is empty, just return a list with our new move
    - Compare our move's distance with the first move in the sorted list
    - If our move is better (lower/equal distance), put it at the front
    - Otherwise, keep the first move and recursively insert into the rest of the list
    
    Example:
    sorted_moves = [moveA(distance=2), moveB(distance=5)]
    new move has distance=3
    Result: [moveA(2), new_move(3), moveB(5)] - maintains sorted order
    
    Args:
        move: Board state to insert into the sorted list
        sorted_moves: Already sorted list of moves (best to worst)
        goal: Goal board for calculating Manhattan distances
        
    Returns:
        List[Board]: New sorted list with the move inserted in correct position
    """
    # Base case: if the sorted list is empty, our move becomes the only item
    if not sorted_moves:
        return [move]
    
    # Calculate how good our new move is (lower distance = better)
    move_distance = manhattan_distance(move, goal)
    
    # Calculate how good the first move in the sorted list is
    first_distance = manhattan_distance(sorted_moves[0], goal)
    
    # Compare distances to decide where to insert
    if move_distance <= first_distance:
        # Our move is better (or equal) - put it at the front
        return [move] + sorted_moves
    else:
        # Our move is worse - keep first move and recursively insert into the rest
        # This will find the correct position further down the list
        return [sorted_moves[0]] + insert_move_by_heuristic(move, sorted_moves[1:], goal)


def sort_moves_by_heuristic(moves: List[Board], goal: Board) -> List[Board]:
    """
    Sort all possible moves by Manhattan distance heuristic (best moves first).
    
    This function takes a list of possible board states and sorts them so that
    the most promising moves (lowest Manhattan distance) come first. This way,
    when we try to solve the puzzle, we explore the best options first.
    
    How it works: Uses insertion sort implemented recursively.
    - Start with an empty sorted list
    - Take moves one by one from the unsorted list
    - Insert each move into the correct position in the sorted list
    - Continue until all moves are sorted
    
    Example:
    Input: [moveA(distance=5), moveB(distance=2), moveC(distance=7)]
    Output: [moveB(2), moveA(5), moveC(7)] - sorted from best to worst
    
    Args:
        moves: List of possible board states to sort
        goal: Goal board for calculating heuristic distances
        
    Returns:
        List[Board]: Moves sorted by heuristic (best moves first)
    """
    # Internal recursive function that does the actual sorting work
    def sort_moves(unsorted: List[Board], sorted_result: List[Board]) -> List[Board]:
        # Base case: no more unsorted moves, return the completed sorted list
        if not unsorted:
            return sorted_result
        
        # Recursive case: take first move from unsorted list and insert it properly
        # into sorted list, then continue with remaining unsorted moves
        return sort_moves(
            unsorted[1:],  # Remaining unsorted moves (all except first)
            insert_move_by_heuristic(unsorted[0], sorted_result, goal)  # Insert first move
        )
    
    # Start the sorting process with all moves unsorted and empty sorted list
    return sort_moves(moves, [])


def is_move_promising(move: Board, goal: Board, current_distance: int) -> bool:
    """
    Check if a move is worth exploring based on heuristic (early pruning).
    
    This is an optimization that helps us avoid wasting time on obviously bad moves.
    The idea is: if a move makes our Manhattan distance much worse, it's probably
    not going to lead to a good solution, so we can skip it entirely.
    
    However, we can't be too strict because sometimes you need to make moves that
    temporarily make things "worse" in order to unblock tiles and make progress.
    That's why we allow some tolerance (+2).
    
    The logic: "Only explore this move if it doesn't make our heuristic distance
    much worse than our current position."
    
    Example scenarios:
    Current distance = 6
    Move A results in distance = 5  ✓ PROMISING (5 ≤ 6 + 2 = 8)
    Move B results in distance = 8  ✓ PROMISING (8 ≤ 6 + 2 = 8)
    Move C results in distance = 9  ✗ NOT PROMISING (9 > 6 + 2 = 8)
    Move D results in distance = 15 ✗ NOT PROMISING (15 > 6 + 2 = 8)
    
    Why +2? This allows for temporary "backward" moves needed to unblock tiles,
    while still filtering out moves that are clearly going in the wrong direction.
    
    Args:
        move: Board state to evaluate for promise
        goal: Target goal state to measure distance to
        current_distance: Current heuristic distance before this move
        
    Returns:
        bool: True if move seems worth exploring, False if we should skip it
    """
    # Calculate how far this move would put us from the goal
    next_distance = manhattan_distance(move, goal)
    
    # Allow moves that don't make distance much worse (tolerance of +2)
    return next_distance <= current_distance + 2


def solve(board: Board, goal: Board, path: List[Board] = None, max_depth: int = 40) -> Optional[List[Board]]:
    """
    Solve puzzle using functional approach with path-based cycle detection.
    
    This is the heart of our 8-puzzle solver. It uses several functional techniques:
    
    1. **Heuristic Search**: Uses Manhattan distance to guide the search toward
       promising moves instead of trying moves randomly.
    
    2. **Path-Based Cycle Detection**: Prevents cycles by checking only the current path,
       allowing different branches to explore states independently.
    
    3. **Pure Functional Design**: No shared state between branches, each recursive
       call operates independently with its own path context.
    
    4. **Move Ordering**: Tries the most promising moves first to find solutions faster.
    
    5. **Depth Limiting**: Prevents stack overflow by limiting how deep we search.
    
    The algorithm works like this:
    1. Check if we're done (current board = goal) → return solution if yes
    2. Check if we should give up (too deep, taking too long) → return failure if yes
    3. Generate all possible next moves (up/down/left/right)
    4. Sort moves by quality (Manhattan distance heuristic)
    5. Try each move in order until we find a solution or run out of moves
    
    Why these optimizations matter:
    - Without heuristics: might try millions of random moves
    - Without cycle detection: might get stuck in infinite loops
    - Without depth limiting: might run forever or crash the program
    - Without move ordering: might find solutions very slowly
    
    Args:
        board: Current board state we're exploring
        goal: Target goal state we want to reach
        path: List of board states showing how we got here (default: None, will be initialized)
        max_depth: Maximum search depth to prevent stack overflow (default: 40)
        
    Returns:
        Optional[List[Board]]: 
        - If solution found: Complete path from start to goal
        - If no solution: None
        
    Example successful return:
    [initial_board, move1_board, move2_board, goal_board] - shows the solution steps
    """
    # Initialize path if this is the first call to solve()
    if path is None:
        path = [board]
    
    # Early termination: give up if we've searched too deep
    # This prevents stack overflow and avoids wasting time on very long paths
    if len(path) > max_depth:
        return None  # Search too deep, give up on this path
    
    # Success condition: check if we've reached the goal!
    if board == goal:
        return path  # Found solution! Return the complete path
    
    # Calculate current heuristic distance for pruning decisions
    current_distance = manhattan_distance(board, goal)
    
    # Path-based cycle detection
    if board in path[:-1]:
        return None
    
    # Relaxed pruning for hard puzzles
    if len(path) > 25 and current_distance > len(path) * 1.3:
        return None
    
    possible_moves = next_states(board)
    sorted_moves = sort_moves_by_heuristic(possible_moves, goal)
    
    # Try each promising move
    for next_board in sorted_moves:
        if (next_board not in path and 
            is_move_promising(next_board, goal, current_distance)):
            
            result = solve(next_board, goal, path + [next_board], max_depth)
            if result:
                return result
    
    return None


def print_board(board: Board) -> None:
    """
    Display board with ASCII art.
    Note: This function has side effects (printing) - not pure functional.
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
    Demonstrate functional 8-puzzle solver.
    Shows immutability: original board unchanged after solving.
    """
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
    
    # Pure functional call - no mutations
    solution = solve(initial_board, goal_board)
    
    if solution:
        print(f"Solution found in {len(solution) - 1} moves:")
        
        for i, board_state in enumerate(solution):
            print(f"Step {i}:")
            print_board(board_state)
    else:
        print("No solution found.")
    
    # Demonstrate immutability
    print("Original board after solving (unchanged):")
    print_board(initial_board)
    
if __name__ == "__main__":
    main()
