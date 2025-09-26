def check_sudoku(board):

    for row in board:
        if sorted(row) != list(range(1, 10)):
            return False

    for c in range(9):
        col = [board[r][c] for r in range(9)]
        if sorted(col) != list(range(1, 10)):
            return False

    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            block = [board[r][c] for r in range(br, br+3) for c in range(bc, bc+3)]
            if sorted(block) != list(range(1, 10)):
                return False

    return True
    
import time
start = time.time()
class Node:
    def __init__(self):
        self.L = self.R = self.U = self.D = self
        self.C = None

class Column(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.size = 0

def iterate(node, attr):
    nxt = getattr(node, attr)
    while nxt != node:
        yield nxt
        nxt = getattr(nxt, attr)

def cover(c):
    c.R.L, c.L.R = c.L, c.R
    for i in iterate(c, 'D'):
        for j in iterate(i, 'R'):
            j.D.U, j.U.D = j.U, j.D
            j.C.size -= 1

def uncover(c):
    for i in iterate(c, 'U'):
        for j in iterate(i, 'L'):
            j.C.size += 1
            j.D.U, j.U.D = j, j
    c.R.L, c.L.R = c, c

def sudoku_solver(board):
    header = Column("root")
    columns = []

    prev = header
    for i in range(324):
        col = Column(i)
        col.R, col.L = prev.R, prev
        prev.R.L, prev.R = col, col
        columns.append(col)
        prev = col

    def add_row(cols, row_cols):
        first = None
        for c in row_cols:
            node = Node()
            col = cols[c]
            node.C = col
            col.size += 1
            node.U, node.D = col.U, col
            col.U.D, col.U = node, node
            if first is None:
                first = node
                first.L = first.R = first
            else:
                node.L, node.R = first.L, first
                first.L.R, first.L = node, node
        return first

    rows = []
    for r in range(9):
        for c in range(9):
            for d in range(1, 10):
                b = (r//3)*3 + (c//3)
                row = [
                    9*r + c,        
                    81 + 9*r + (d-1), 
                    162 + 9*c + (d-1),
                    243 + 9*b + (d-1) 
                ]
                rows.append((r, c, d, add_row(columns, row)))

    solution = []

    def search():
        if header.R == header:
            return True

        # choose min column
        c = header.R
        min_c = c
        s = c.size
        while c != header:
            if c.size < s:
                s = c.size
                min_c = c
            c = c.R
        c = min_c

        cover(c)
        for r in iterate(c, 'D'):
            solution.append(r)
            for j in iterate(r, 'R'):
                cover(j.C)
            if search():
                return True
            for j in iterate(r, 'L'):
                uncover(j.C)
            solution.pop()
        uncover(c)
        return False

    for r in range(9):
        for c in range(9):
            d = board[r][c]
            if d != 0:
                b = (r//3)*3 + (c//3)
                row = [
                    9*r + c,
                    81 + 9*r + (d-1),
                    162 + 9*c + (d-1),
                    243 + 9*b + (d-1)
                ]
                row_nodes = []
                first = None
                for idx in row:
                    col = columns[idx]
                    node = col.U
                    while True:
                        if hasattr(node, 'C') and node.C == col:
                            break
                        node = node.U
                    first = node
                    break
                for tup in rows:
                    if tup[0] == r and tup[1] == c and tup[2] == d:
                        node = tup[3]
                        for j in iterate(node, 'R'):
                            cover(j.C)
                        cover(node.C)
                        solution.append(node)
                        break

    if search():
        ans = [[0]*9 for _ in range(9)]
        for r in solution:
            row = r
            nums = []
            nums.append(row)
            for j in iterate(r, 'R'):
                nums.append(j)
            rc, rd, cc, bc = sorted([n.C.name for n in nums])
            rr = rc // 9
            cc = rc % 9
            d = (rd - 81) % 9 + 1
            ans[rr][cc] = d
        return ans
    else:
        return None
"""
puzzle = [
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0]
]
"""
puzzle = [
    [2,0,0, 0,0,0, 0,7,4],
    [0,0,0, 5,0,1, 0,0,0],
    [8,0,0, 0,0,0, 0,0,0],
    [0,3,0, 6,0,0, 1,0,0],
    [4,0,0, 0,0,0, 0,0,0],
    [0,7,0, 0,0,0, 0,0,0],
    [0,0,0, 0,4,0, 0,8,0],
    [0,0,1, 0,0,0, 5,0,0],
    [0,6,0, 0,0,0, 0,0,0]
]
"""
puzzle = [
    [0,0,0, 2,6,0, 7,0,1],
    [6,8,0, 0,7,0, 0,9,0],
    [1,9,0, 0,0,4, 5,0,0],
    [8,2,0, 1,0,0, 0,4,0],
    [0,0,4, 6,0,2, 9,0,0],
    [0,5,0, 0,0,3, 0,2,8],
    [0,0,9, 3,0,0, 0,7,4],
    [0,4,0, 0,5,0, 0,3,6],
    [7,0,3, 0,1,8, 0,0,0],
]
"""
solution = sudoku_solver(puzzle)
for row in solution:
    print(row)

stop = time.time()
print(check_sudoku(solution))
print(f"{(stop - start) * 1000:.5f} ms")


start2 = time.time()
def find_empty(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c
    return None

def valid(board, r, c, num):
    if num in board[r]:
        return False

    if num in [board[i][c] for i in range(9)]:
        return False
    br, bc = (r // 3) * 3, (c // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[br+i][bc+j] == num:
                return False
    return True

def solve_sudoku(board):
    empty = find_empty(board)
    if not empty:
        return True
    r, c = empty
    for num in range(1, 10):
        if valid(board, r, c, num):
            board[r][c] = num
            if solve_sudoku(board):
                return True
            board[r][c] = 0
    return False

solve_sudoku(puzzle)   

for row in puzzle:
    print(row)

stop2 = time.time()
print(check_sudoku(puzzle))
print(f"{(stop2 - start2) * 1000:.5f} ms")
