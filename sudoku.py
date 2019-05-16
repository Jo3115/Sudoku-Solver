import random
import math


class Node:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.contendors = []
        self.square = []
        self.square.append(math.trunc(self.x/3)*3)
        self.square.append(math.trunc(self.y/3)*3)

    def populate_contendors(self, board):
        self.contendors = []
        for x in range(9):
            self.contendors.append(board[x][self.y].value)
        for y in range(9):
            self.contendors.append(board[self.x][y].value)
        for x in range(3):
            for y in range(3):
                self.contendors.append(board[x+self.square[0]][y+self.square[1]].value)


def create_board():
    board = [[None for _ in range(9)] for _ in range(9)]
    for x in range(9):
        for y in range(9):
            board[x][y] = Node(x,y, None)
    clues = 30
    while clues != 0:
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        while board[x][y].value is None:
            number = random.randint(1,9)
            if number not in board[x][y].contendors:
                board[x][y].value = number
                update_contendors(board)
        clues -= 1
    board = convert_node_board(board)
    return board


def print_board(board):
    loop = 0
    for x in range(9):
        for y in range(9):
            if board[x][y] == None:
                board[x][y] = " "
    board = [[str(y) for y in x] for x in board]
    while loop < 9:
        print("------------------")
        print("|"+board[loop][0]+" "+board[loop][1]+" "+board[loop][2]+"|"+
              board[loop][3]+" "+board[loop][4]+" "+board[loop][5]+"|"+
              board[loop][6]+" "+board[loop][7]+" "+board[loop][8]+"|")
        print("|"+board[loop+1][0]+" "+board[loop+1][1]+" "+board[loop+1][2]+
              "|"+board[loop+1][3]+" "+board[loop+1][4]+" "+board[loop+1][5]+
              "|"+board[loop+1][6]+" "+board[loop+1][7]+" "+board[loop+1][8]+
              "|")
        print("|"+board[loop+2][0]+" "+board[loop+2][1]+" "+board[loop+2][2]+
              "|"+board[loop+2][3]+" "+board[loop+2][4]+" "+board[loop+2][5]+
              "|"+board[loop+2][6]+" "+board[loop+2][7]+" "+board[loop+2][8]+
              "|")
        loop += 3
    print("------------------")


def save_board(board):
    file = open("output.txt", "w")
    loop = 0
    for x in range(9):
        for y in range(9):
            if board[x][y] is None:
                board[x][y] = " "
    board = [[str(y) for y in x] for x in board]
    while loop < 9:
        file.write("------------------"+"\n"+"|"+board[loop][0]+" "+
                   board[loop][1]+" "+board[loop][2]+"|"+board[loop][3]+" "+
                   board[loop][4]+" "+board[loop][5]+"|"+board[loop][6]+" "+
                   board[loop][7]+" "+board[loop][8]+"|"+"\n"
                   +"|"+board[loop+1][0]+" "+board[loop+1][1]+" "+
                   board[loop+1][2]+"|"+board[loop+1][3]+" "+board[loop+1][4]
                   +" "+board[loop+1][5]+"|"+board[loop+1][6]+" "+
                   board[loop+1][7]+" "+board[loop+1][8]+"|"+"\n"
                   +"|"+board[loop+2][0]+" "+board[loop+2][1]+" "+
                   board[loop+2][2]+"|"+board[loop+2][3]+" "+
                   board[loop+2][4]+" "+board[loop+2][5]+"|"+board[loop+2][6]+
                   " "+board[loop+2][7]+" "+board[loop+2][8]+"|"+"\n")
        loop += 3
    file.write("------------------")
    file.close


def start_create_board():
    board = create_board()
    choice = input("would you like to output in a file?[Y][N]")
    if (choice == "Y"):
        save_board(board)


def import_board():
    file = open("input.txt","r")
    lines = file.readlines()
    file.close
    board = [[None for _ in range(9)] for _ in range(9)]
    del lines[0]
    del lines[3]
    del lines[6]
    for x in range(9):
        for y in range(9):
            character = (lines[x])[(y*2)+1]
            if (character != " "):
                if character != "\n":
                    board[x][y] = character
    print_board(board)
    return (board)
        
      
def test_board(board):
    for x in range(9):
        for y in range(9):
            if board[x][y].value is not None:
                board[x][y].contendors.remove(board[x][y].value)
                board[x][y].contendors.remove(board[x][y].value)
                board[x][y].contendors.remove(board[x][y].value)
                if board[x][y].value in board[x][y].contendors:
                    return False
    return True


def convert_node_board(board_nodes):
    board_new = [[" " for _ in range(9)] for _ in range(9)]
    for x in range(9):
        for y in range(9):
            if board_nodes[x][y].value is not None:
                board_new[x][y] = str(board_nodes[x][y].value)
    print_board(board_new)
    return board_new


def solve_board_main():
    board = import_board()
    board = convert_board_for_solve(board)
    boardNode = create_nodes(board)
    if test_board(boardNode):
        solved_board = solve_board(boardNode, [0, 0])
        solved_board = convert_node_board(solved_board[0])
        choice = input("would you like to output in a file?[Y][N]")
        if (choice == "Y"):
            save_board(solved_board)
    else:
        print('invalid board')


def create_nodes(board):
    boardNodes = [[None for _ in range(9)] for _ in range(9)]
    for x in range(9):
        for y in range(9):
            boardNodes[x][y] = Node(x,y,board[x][y])
    update_contendors(boardNodes)
    return boardNodes


def update_contendors(board_nodes):
    for x in range(9):
        for y in range(9):
            board_nodes[x][y].populate_contendors(board_nodes)


def solve_board(board_node, positon):
    empty_position = find_empty(board_node, positon)
    try:
        x = empty_position[0]
        y = empty_position[1]
    except:
        return [board_node, 'final']
    board_node[x][y].populate_contendors(board_node)
    contendors = board_node[x][y].contendors
    for i in contendors:
        if i is None:
            contendors.remove(i)
    options = [1,2,3,4,5,6,7,8,9]
    for i in contendors:
        if i in options:
            options.remove(i)
    if len(options) == 0:
        return board_node
    for number in options:
        board_node[x][y].value = number
        #convert_node_board(boardNode)
        board_node[x][y].populate_contendors(board_node)
        board_node = solve_board(board_node, empty_position)
        if 'final' in board_node:
            return board_node
        board_node[x][y].value = None
    return board_node


def find_empty(board,emptyPositions):
    for x in range(9):
        for y in range(9):
            if board[x][y].value == None:
                emptyPositions[0] = x
                emptyPositions[1] = y
                return emptyPositions


def convert_board_for_solve(board):
    boardNew = [[None for _ in range(9)] for _ in range(9)]
    for x in range(9):
        for y in range(9):
            if board[x][y] != " ":
                boardNew[x][y] = int(board[x][y])
    board = boardNew
    return board


def main():
    choice = input ("""would you like to:
    [C] create a Board
    [T] test a Board
    [S] solve a Board
    : """)
    if choice == "C":
        start_create_board()
    elif choice == "T":
        board = import_board();
        board = convert_board_for_solve(board)
        boardNode = create_nodes(board)
        print("Is the Board Valid True Or False: " + str(test_board(boardNode)))
    elif choice == "S":
        solve_board_main()
    elif choice == "CS":
        create_solve()


if __name__ == '__main__':
    main()
