import random

def initial_board(n):
    board = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        j = random.randint(0, n-1)
        board[i][j] = i+1
    return board

def print_board(board): 
    for row in board: 
        row_str = ""
        for cell in row:
            if cell == 0:
                row_str += "0 "
            else:
                row_str += str(cell) + " "
        print(row_str.strip())

def count_conflicts(board, row, col):
    n = len(board)
    count = 0
    for i in range(n):
        if i != row and board[i][col] != 0:
            count += 1
        if i != col and board[row][i] != 0:
            count += 1
    for i in range(1, n):
        if row-i >= 0 and col-i >= 0 and board[row-i][col-i] != 0:
            count += 1
        if row-i >= 0 and col+i < n and board[row-i][col+i] != 0:
            count += 1
        if row+i < n and col-i >= 0 and board[row+i][col-i] != 0:
            count += 1
        if row+i < n and col+i < n and board[row+i][col+i] != 0:
            count += 1
    return count

def find_conflicts(board):
    n = len(board)
    conflicts = {}
    for i in range(n):
        for j in range(n):
            if board[i][j] != 0:
                conflicts[(i,j)] = count_conflicts(board, i, j)
    return conflicts

def find_empty_positions(board):
    empty_positions = []
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                empty_positions.append((i, j))
    return empty_positions

def move_queen(board, row, col):
    n = len(board)
    conflicts = find_conflicts(board)
    max_conflicts = conflicts[(row, col)]
    max_conflict_positions = [(r, c) for (r, c), count in conflicts.items() if count == max_conflicts]
    empty_positions = find_empty_positions(board)
    min_conflicts = float('inf')
    min_conflict_positions = []
    for r, c in max_conflict_positions:
        for i, j in empty_positions:
            new_board = [row[:] for row in board]
            new_board[r][c], new_board[i][j] = new_board[i][j], new_board[r][c]
            conflicts = find_conflicts(new_board)
            count = conflicts[(i, j)]
            if count < min_conflicts:
                min_conflicts = count
                min_conflict_positions = [(i, j)]
            elif count == min_conflicts:
                min_conflict_positions.append((i, j))
    if min_conflict_positions:
        r, c = random.choice(min_conflict_positions)
        board[row][col], board[r][c] = board[r][c], board[row][col]
        return r, c
    else:
        return row, col

def solve_n_queens():
    n = int(input("Enter the board size: "))
    while n == 2 or n == 3:
        print("Solution does not exist. Please enter a board size not equal to 2 or 3:")
        n = int(input("Enter the board size: "))
    board = initial_board(n)
    print("Initial board:")
    print_board(board)
    moves = 0
    while True:
        conflicts = find_conflicts(board)
        if all(conflicts[pos] == 0 for pos in conflicts):
            break
        pos = max(conflicts, key=conflicts.get)
        row, col = pos
        row, col = move_queen(board, row, col)
        board[row][col], board[row][col] = board[row][col], 0
        moves += 1
        #move queen to a less conflicting position
        current_conflicts = count_conflicts(board, row, col)
        less_conflict_pos = []
        for i in range(n):
            for j in range(n):
                if board[i][j] == 0:
                    new_conflicts = count_conflicts(board, i, j)
                    if new_conflicts < current_conflicts:
                        less_conflict_pos.append((i,j))
        if less_conflict_pos:
            row, col = random.choice(less_conflict_pos)
            board[row][col], board[row][col] = board[row][col], 0
    print("Final board:")
    print_board(board)
    print(f"Solved in {moves} moves.")
def main():
    solve_n_queens()
if __name__ == '__main__':
    main()
