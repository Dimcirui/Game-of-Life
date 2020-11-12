import os
import random
import pandas as pd

''' 
Adding the sentence below in order to avoid 'using before assignment' errors.
Actually this program runs normally even without this sentence. But I don't know why at present.
'''
board1, board2 = {}, {}

# Rules part ('*' means a live cell, ' ' means a dead cell)
def run(size) :
    global board1,board2

    count = 0

    ## Interactions.
    for i in range(0,size-1) :
        for j in range(0,size-1) :
                #### Count the numbers of live cells. If this happens at the edge, those outside the edge will be ignored. 
                for x in range(3) :
                    for y in range(3) :
                        if (i+x-1 <0 or i+x-1 > size-1 or j+y-1 <0 or j+y-1 > size-1) :
                            continue
                        elif (x*y != 1 and board1[str(i+x-1)][j+y-1] == '*') :
                            count += 1
                #### Run the rules. The result will be stored in board2.
                if (board1[str(i)][j] == ' ' and count == 3) :
                    board2[str(i)][j] = '*'
                elif (board1[str(i)][j] == '*' and (count == 2 or count == 3)) :
                    board2[str(i)][j] = board1[str(i)][j]
                else :
                    board2[str(i)][j] = ' '

                count = 0
    ## Copy board2 to board1, then initialize board2.
    board1 = board2.copy()
    board2 = {'{}'.format(i):[' ']*size for i in range(size)}


# Operation part
if __name__ == '__main__' :
    ## Generate initial chessboard(board1).
    size = eval(input('Please enter the size of chessboard (n*n): '))
    board1 = {'{}'.format(i):[' ']*size for i in range(size)}
    ## Generate a same-size blank chessboard(board2), which is used for storing the result.
    board2 = {'{}'.format(i):[' ']*size for i in range(size)}
    ## Add specified number of live cells to board1.
    num = eval(input('Please enter the number of live cells initially generated: '))
    for j in range(num) :
        r1 = random.randint(0,size-1)
        r2 = random.randint(0,size-1)
        while (board1[str(r1)][r2] == '*') :
            r1 = random.randint(0,size-1)
            r2 = random.randint(0,size-1)
        else :
            board1[str(r1)][r2] = '*'
    ## Show board1.
    screen = pd.DataFrame(board1)
    print(screen)

    ## Start
    while True :
        key = input('Continue or not? Enter \'y\' to continue，enter \'n\' to exit.\n')
        if 'y' == key :
            os.system('cls')
            run(size)
            screen = pd.DataFrame(board1)
            print(screen)
        elif 'n' == key :
            print('Good Bye!\n')
            break
        else :
            print('Did you enter the right word? Please keyboard again.\n')
            continue
