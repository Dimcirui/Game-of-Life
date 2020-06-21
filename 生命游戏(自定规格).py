#! usr/bin/env python3

import random
import pandas as pd

'''
生命游戏规则简介：
每个细胞有两种状态——存活或死亡，每个细胞与以自身为中心的周围八格细胞产生互动。

当前细胞为死亡状态时，当周围有3个存活细胞时，该细胞变成存活状态。
当前细胞为存活状态时，当周围有2个或3个存活细胞时， 该细胞保持原样。
当前细胞为存活状态时，当周围有2个以下存活细胞时， 该细胞变成死亡状态。
当前细胞为存活状态时，当周围有3个以上的存活细胞时，该细胞变成死亡状态。
'''

#规则部分（活细胞为'*'，死细胞为' '）
def run(size) :
    global board1,board2
    ##计数初始为0
    count = 0
    ##边界判断，从第一行第一列开始判断并执行，一直循环到最后一行最后一列。判断得到的结果储存在新棋盘内。
    for i in range(0,size-1) :
        for j in range(0,size-1) :
                ####统计周围8格活细胞的数量，如果在棋盘外，则除去
                for x in range(3) :
                    for y in range(3) :
                        if (i+x-1 <0 or i+x-1 > size-1 or j+y-1 <0 or j+y-1 > size-1) :
                            continue
                        elif (x*y != 1 and board1[str(i+x-1)][j+y-1] == '*') :
                            count += 1
                ####判断、存储开始
                if (board1[str(i)][j] == ' ' and count == 3) :
                    board2[str(i)][j] = '*'
                elif (board1[str(i)][j] == '*' and (count == 2 or count == 3)) :
                    board2[str(i)][j] = board1[str(i)][j]
                else :
                    board2[str(i)][j] = ' '
                ####单格判断结束后，计数初始化，并开始下一格
                count = 0
    ##将判断后得到的新棋盘覆盖到初始棋盘上，并将新棋盘初始化
    board1 = board2.copy()
    board2 = {'{}'.format(i):[' ']*size for i in range(size)}


#游戏运行部分
if __name__ == '__main__' :
    ##生成初始棋盘（n*n）
    size = eval(input('请输入棋盘规格（n*n）：'))
    board1 = {'{}'.format(i):[' ']*size for i in range(size)}
    ##生成新的空棋盘，以用于存储运行结果
    board2 = {'{}'.format(i):[' ']*size for i in range(size)}
    ##随机添加n个活细胞
    num = eval(input('请输入随机生成的活细胞的数量：'))
    for j in range(num) :
        r1 = random.randint(0,size-1)
        r2 = random.randint(0,size-1)
        while (board1[str(r1)][r2] == '*') :
            r1 = random.randint(0,size-1)
            r2 = random.randint(0,size-1)
        else :
            board1[str(r1)][r2] = '*'
    ##展示初始棋盘
    screen1 = pd.DataFrame(board1)
    print(screen1)

    ##开始迭代
    while True :
        key = input('是否进行下一轮迭代？输入next以继续，输入end以退出。\n')
        if 'next' == key :
            run(size)
            screen1 = pd.DataFrame(board1)
            print(screen1)
        elif 'end' == key :
            print('再见！\n')
            break
        else :
            print('您确定您打对字了？请重新输入。\n')
            continue
