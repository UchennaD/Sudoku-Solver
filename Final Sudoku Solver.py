from tkinter import *

#Solver Code
def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else: 
        row, col = find

    for i in range(1,10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True
            
            bo[row][col] = 0
    
    return False




def valid(bo, num, pos):
    # check row
    for i in range (len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False
        
    #check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False
        
    #check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False
    
    return True

 
def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- " * 16)

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end ="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end=" ")

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j) #row, col
    
    return None


#print_board(board)
#solve(board)
#print("Solved: ")
#print_board(board)


#GUI Code

root = Tk()
root.title("Sudoku Solver")
root.geometry("324x550")
label=Label(root,text="Fill in the numbers and click solve").grid(row=0,column=1,columnspan=10)

errLabel=Label(root,text="",fg="red")
errLabel.grid(row=15,column=1,columnspan=10,pady=5)

solvedLabel=Label(root,text="",fg="green")
solvedLabel.grid(row=15,column=1,columnspan=10,pady=5)

cells = {}

def ValidateNumber(P):
    out=(P.isdigit()or P=="") and len(P)<2
    return out 

reg = root.register(ValidateNumber)

def draw3x3Grid(row,column,bgcolor):
    for i in range(3):
        for j in range(3):
            e = Entry(root, width=5,bg=bgcolor,justify="center",validate="key",validatecommand=(reg,"%P"))
            e.grid(row=row+i+1,column=column+j+1,sticky="nsew",padx=1,pady=2,ipady=5)
            cells[(row+i+1,column+j+1)]=e

def draw9x9Grid():
    color="#e799f4"
    for rowNo in range(1,10,3):
        for colNo in range(0,9,3):
            draw3x3Grid(rowNo,colNo,color)
            if color =="#e799f4":
                color = "#dbdbdb"
              
            else:
                color =="#e799f4"

def clearValues():
    errLabel.configure(text="")
    solvedLabel.configure(text="")
    for row in range(2,11):
        for col in range(1,10):
            cell = cells[(row,col)]
            cell.delete(0,"end")

def updateValue(board):
    for row in range(2, 11):
        for col in range(1, 10):
            cell = cells[(row, col)]
            cell.delete(0, "end")
            cell.insert(0, str(board[row - 2][col - 1]))

def getValues():
    board=[]
    errLabel.configure(text="")
    solvedLabel.configure(text="")
    for row in range(2,11):
        rows = []
        for col in range(1,10):
            val = cells[(row,col)].get()
            if val == "":
                rows.append(0)
            else:
                rows.append(int(val))

        board.append(rows)
    return board
import logging

def solveButton():
    # Get the values from the GUI
    board = getValues()

    logging.debug(board)

    # Solve the Sudoku puzzle
    if board is not None: 
        solved = solve(board)

    # Update the GUI with the solved puzzle

        if solved:
            updateGrid(board)
        else:
            errLabel.configure(text="Sudoku puzzle is unsolvable")

btn = Button(root,command=solveButton,text="Solve",width=10)
btn.grid(row=20,column=1,columnspan=5,pady=20)

btn = Button(root,command=clearValues,text="Clear",width=10)
btn.grid(row=20,column=5,columnspan=5,pady=20)

def board_is_solved(bo):
    for row in bo:
        if 0 in row:
            return False
    return True

def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- " * 16)

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end=" ")

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

def updateGrid(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                cells[(i + 2, j + 1)].delete(0, "end")
                cells[(i + 2, j + 1)].insert(0, str(board[i][j]))


draw9x9Grid()
root.mainloop()