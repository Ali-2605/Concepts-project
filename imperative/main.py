from typing import List, Optional
import heapq 

Board = List[List[int]]

def copy_board(board: Board) -> Board:
    new_board: Board = []
    for row in board:
        new_board.append(row[:])
    return new_board

def board_to_string(board: Board) -> str:
    result = ""
    for row in board:
        for value in row:
            result = result + f"{value}"
    return result

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

def get_neighbors(board: Board, zero_row: int, zero_col: int) -> List:
    neighbors = []
    zero_positions = []
    
    directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    
    for dr, dc in directions:
        new_row = zero_row + dr
        new_col = zero_col + dc
        
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_board = copy_board(board)
            new_board[zero_row][zero_col], new_board[new_row][new_col] = \
                new_board[new_row][new_col], new_board[zero_row][zero_col]
            zero_pos = []
            zero_pos.extend([new_row, new_col])
            neighbors.append(new_board), zero_positions.append(zero_pos)
    
    result = []
    result.extend([neighbors, zero_positions])
    return result

def a_star_search(start: Board, goal: Board, max_iterations: int = 100000) -> Optional[List[Board]]:
    start_hash = board_to_string(start)
    goal_hash = board_to_string(goal)

    zero_row = 0
    zero_col = 0
    for row in range(len(start)):
        for col in range(len(start[row])):
            if start[row][col] == 0:
                zero_row = row
                zero_col = col

    open_set_item = []
    open_set_item.extend([manhattan_distance(start, goal), 0, start, [start], zero_row, zero_col])
    
    open_set = []
    heapq.heappush(open_set, (manhattan_distance(start, goal), 0, start_hash, open_set_item))
    
    closed_set = []
    g_score = {start_hash: 0}
    counter = 1
    iterations = 0

    while open_set and iterations < max_iterations:
        iterations += 1

        f_score, _, current_hash, current_item = heapq.heappop(open_set)
        current_board = current_item[2]
        path = current_item[3]
        current_zero_row = current_item[4]
        current_zero_col = current_item[5]
        
        current_hash = board_to_string(current_board)

        if current_hash == goal_hash:
            return path

        closed_set.append(current_hash)
        current_g = g_score[current_hash]

        result = get_neighbors(current_board, current_zero_row, current_zero_col)
        neighbors = result[0]
        zero_positions = result[1]
        
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            neighbor_zero_row = zero_positions[i][0]
            neighbor_zero_col = zero_positions[i][1]
            neighbor_hash = board_to_string(neighbor)

            found = False
            for item in closed_set:
                if item == neighbor_hash:
                    found = True
                    break
            
            if found:
                continue

            tentative_g = current_g + 1

            if neighbor_hash not in g_score or tentative_g < g_score[neighbor_hash]:
                g_score[neighbor_hash] = tentative_g
                h_score = manhattan_distance(neighbor, goal)
                f = tentative_g + h_score

                path_copy = []
                for board in path:
                    path_copy.append(copy_board(board))
                path_copy.append(copy_board(neighbor))

                new_item = []
                new_item.extend([f, counter, copy_board(neighbor), path_copy, neighbor_zero_row, neighbor_zero_col])
                
                heapq.heappush(open_set, (f, counter, neighbor_hash, new_item))
                counter += 1

    return None

def print_board(board: Board) -> None:
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
    
    print("\nInitial Board:")
    print_board(initial_board)
    
    print("Goal Board:")
    print_board(goal_board)
    
    print("Solving...\n")

    solution = a_star_search(initial_board, goal_board)
    
    if solution:
        print(f"Solution found in {len(solution) - 1} moves:\n")
        
        for i, board_state in enumerate(solution):
            print(f"Step {i}:")
            print_board(board_state)
    else:
        print("No solution found within iteration limit.")

if __name__ == "__main__":
    main()
