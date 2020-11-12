from tkinter import *
import tkinter.messagebox as mb 
import tkinter.simpledialog as sd
import random as rd
import time

class Game_of_Life():
    def __init__(self):
        self.GoL = Tk()
        self.prog_width = 728   #程序宽度
        self.prog_height = 550  #程序高度
        self.game_size = 450    #游戏画面尺寸（正方形）
        self.size = 40          #初始棋盘规格
        self.auto_speed = 250   #自动迭代速度x2（毫秒） 
        self.sample = ['预设棋盘', '闪烁者', '方块', '蜂巢', '滑翔器', 'Gosper滑翔枪', 'π', '轻型飞船', '轻型飞船+吞噬者', '开关引擎', '脉冲星']
        self.auto_flag = False  #自动状态判断

    #核心规则部分（活细胞为'*'，死细胞为' '）
    def core(self):
        ##计数初始为0
        count = 0
        ##边界判断，从第一行第一列开始判断并执行，一直循环到最后一行最后一列。判断得到的结果储存在新棋盘内。
        for i in range(0, self.size-1):
            for j in range(0, self.size-1):
                    ###统计周围8格活细胞的数量，如果在棋盘外，则除去
                    for x in range(3):
                        for y in range(3):
                            if (i+x-1 <0 or i+x-1 > self.size-1 or j+y-1 <0 or j+y-1 > self.size-1):
                                continue
                            elif (x*y != 1 and self.board1[str(i+x-1)][j+y-1] == '*'):
                                count += 1
                    ###判断、存储开始
                    if (self.board1[str(i)][j] == ' ' and count == 3):
                        self.board2[str(i)][j] = '*'
                    elif (self.board1[str(i)][j] == '*' and (count == 2 or count == 3)):
                        self.board2[str(i)][j] = self.board1[str(i)][j]
                    else:
                        self.board2[str(i)][j] = ' '
                    ###单格判断结束后，计数初始化，并开始下一格
                    count = 0
        ##将判断后得到的新棋盘覆盖到初始棋盘上，并将新棋盘初始化
        self.board1 = self.board2.copy()
        self.board2 = {'{}'.format(i):[' ']*self.size for i in range(self.size)}

    #界面部分
    def set_GoL(self):
        ##底部基础(标题和窗口)
        self.GoL.title('生命游戏')
        self.GoL.geometry('{0}x{1}+100+100'.format(self.prog_width, self.prog_height))
        ##游戏画面
        self.game_GoL = Canvas(self.GoL, width=self.game_size, height=self.game_size, bg='white')
        self.game_GoL.grid(row=0, column=0, rowspan=2, columnspan=2, padx=5, pady=5)
        ##按钮
        self.auto_button = Button(self.GoL, text='自动生成', command=self.auto_collect)
        self.auto_button.grid(row=0, column=2, columnspan=2)
        self.manual_button = Button(self.GoL, text='手动生成', command=self.manual_collect)
        self.manual_button.grid(row=1, column=2)
        self.set_switch_button = Button(self.GoL, text='手动设置细胞：关', command=self.set_switch)
        self.set_switch_button.grid(row=1, column=3)
        self.auto_step_button = Button(self.GoL, text='自动迭代', command=self.auto_step)
        self.auto_step_button.grid(row=2, column=0)
        self.pause_button = Button(self.GoL, text='暂停', command=self.pause)
        self.pause_button.grid(row=3, column=0)
        self.next_step_button = Button(self.GoL, text='下一步', command=self.next_step)
        self.next_step_button.grid(row=2, column=1)
        self.reset_button = Button(self.GoL, text='清空棋盘', command=self.reset)
        self.reset_button.grid(row=3, column=1)
        self.rule_button = Button(self.GoL, text='生命游戏\n说明', command=self.show_rule)
        self.rule_button.grid(row=3, column=2, rowspan=2, columnspan=2)
        self.init_sample_button = Button(self.GoL, text='选择', command=self.init_sample)
        self.init_sample_button.grid(row=2, column=3)
        ##预设键盘复选框
        self.var1 = StringVar()
        self.var1.set('预设棋盘')
        self.init_sample_optionmenu = OptionMenu(self.GoL, self.var1, *self.sample)
        self.init_sample_optionmenu.grid(row=2, column=2)
        ##刷新界面
        self.GoL.after(self.auto_speed, self.refresh)
        ##初始界面
        self.size_set()
        self.show_game()
        ##创建窗口
        self.GoL.mainloop()

    ##规则弹窗
    def show_rule(self):
        mb.showinfo(title='规则', message='''
1、生命游戏规则简介：
    每个细胞有两种状态——存活或死亡，每个细胞与以自身为中心的周围八格细胞产生互动。
    当前细胞为死亡状态时，当周围有3个存活细胞时，该细胞变成存活状态；
    当前细胞为存活状态时，当周围有2个或3个存活细胞时， 该细胞保持原样；
    当前细胞为存活状态时，当周围有2个以下存活细胞时， 该细胞变成死亡状态；
    当前细胞为存活状态时，当周围有3个以上的存活细胞时，该细胞变成死亡状态。
2、按钮简介：
    自动生成：根据输入的棋盘规格和初始活细胞数量生成棋盘，活细胞在棋盘中的随机位置生成。
    手动生成：根据输入的棋盘规格生成棋盘，而后通过鼠标左键手动改变细胞状态。
    预设键盘：使用预设的棋盘进行游戏，规格固定为40x40，按选择以启动。
    自动迭代：每{0}ms进行一次迭代，期间进行其他操作（点击其他按钮）均会停止迭代。
    暂停：暂停自动迭代。
    下一步：手动进行下一次迭代，此后可用鼠标手动改变细胞状态。
    清空棋盘：不改变棋盘规格，清空棋盘上的活细胞。
3、初始棋盘规格为{1}x{2}。
'''.format(self.auto_speed*2, self.size, self.size))
    ##交互式弹窗(获取棋盘规格和初始细胞数量)
    def auto_collect(self):
        self.auto_data = sd.askstring(title='初始化', prompt='初始棋盘边长（建议不超过100）和初始活细胞数量（用英文逗号“,”隔开）：')
        self.auto_set(self.auto_data)
    def manual_collect(self):
        self.manual_data = sd.askinteger(title='初始化', prompt='初始棋盘边长（建议不超过100）：')
        self.manual_set(self.manual_data)

    #自动迭代规则
    def refresh(self):
        self.GoL.after(self.auto_speed, self.refresh)
        if self.auto_flag:
            self.step()

    #设置棋盘规格（生成空棋盘字典）
    def size_set(self):
        self.board1 = {'{}'.format(i):[' ']*self.size for i in range(self.size)}
        self.board2 = {'{}'.format(i):[' ']*self.size for i in range(self.size)}

    #自动生成
    def auto_set(self, datastr):
        self.auto_flag = False
        datalist = datastr.split(',', 1)
        self.size, self.num = eval(datalist[0]), eval(datalist[1])
        self.size_set()
        for j in range(self.num) :
            r1 = rd.randint(0,self.size-1)
            r2 = rd.randint(0,self.size-1)
            while (self.board1[str(r1)][r2] == '*') :
                r1 = rd.randint(0,self.size-1)
                r2 = rd.randint(0,self.size-1)
            else :
                self.board1[str(r1)][r2] = '*'
        self.show_game()

    #手动生成
    def manual_set(self, size):
        self.auto_flag = False
        self.size = size
        self.size_set()
        self.show_game()
        self.mouse_bind()
    ##通过鼠标点击切换细胞状态
    def mouse_bind(self):
        self.set_switch_button['text'] = '手动设置细胞：开'
        self.game_GoL.bind('<Button-1>', self.mouse_set)
    def mouse_set(self, event):
        x, y = int(event.x / self.cell_size), int(event.y / self.cell_size) 
        if x<self.size and y<self.size:
            if self.set_switch_button['text'] == '手动设置细胞：开':
                self.board1[str(x)][y] = '*'
                self.game_GoL.create_rectangle(self.cell_size*x, self.cell_size*y, self.cell_size*(x+1), self.cell_size*(y+1), fill='white')
            else:
                self.board1[str(x)][y] = ' '
                self.game_GoL.create_rectangle(self.cell_size*x, self.cell_size*y, self.cell_size*(x+1), self.cell_size*(y+1), fill='black')

    #手动设置细胞状态开关
    def set_switch(self):
        if self.set_switch_button['text'] == '手动设置细胞：开':
            self.set_switch_button['text'] = '手动设置细胞：关'
            self.game_GoL.unbind('<Button-1>')
        else:
            self.set_switch_button['text'] = '手动设置细胞：开'
            self.mouse_bind()

    #迭代规则
    def step(self):
        self.core()
        self.show_game()
    ##自动迭代
    def auto_step(self):
        self.auto_flag = True
    ##暂停
    def pause(self):
        self.auto_flag = False
    ##下一步（手动迭代）
    def next_step(self):
        self.auto_flag = False
        self.step()

    #清空棋盘
    def reset(self):
        self.auto_flag = False
        self.size_set()
        self.show_game()

    #预设棋盘
    def init_sample(self):
        self.auto_flag = False
        sample = self.var1.get()
        self.size = 40
        self.size_set()
        if sample == '预设棋盘':
            self.show_game()
        elif sample == '闪烁者':
            BlinkerX = [19, 19, 19]
            BlinkerY = [19, 20, 21]
            self.set_cell(BlinkerX, BlinkerY)
        elif sample == '方块':
            BlockX = [19, 19, 20, 20]
            BlockY = [19, 20, 19, 20]
            self.set_cell(BlockX, BlockY)
        elif sample == '蜂巢':
            BeehiveX = [19, 20, 20, 21, 21, 22]
            BeehiveY = [20, 19, 21, 19 ,21, 20]
            self.set_cell(BeehiveX, BeehiveY)
        elif sample == '滑翔器':
            GliderX = [1, 2, 3, 3, 3]
            GliderY = [2, 3, 1, 2, 3]
            self.set_cell(GliderX, GliderY)
        elif sample == 'Gosper滑翔枪':
            GGGX = [1, 1, 2, 2, 10, 10, 10, 11, 11, 12, 12, 13, 13, 14, 15, 15, 16, 16, 16, 17, 20, 20, 20, 21, 21, 21, 22, 22, 24, 24, 24, 24, 34, 34, 35, 35]
            GGGY = [5, 6, 5, 6, 4 , 5 , 6 , 3 , 7 , 2 , 8 , 2 , 8 , 5 , 3 , 7 , 4 , 5 , 6 , 5 , 2 , 3 , 4 , 2 , 3 , 4 , 1 , 5 , 0 , 1 , 5 , 6 , 2 , 3 , 2 , 3 ]
            self.set_cell(GGGX, GGGY)
        elif sample == 'π':
            BreederX = [19, 19, 19, 20, 21, 21, 21]
            BreederY = [19, 20, 21, 19, 19, 20, 21]
            self.set_cell(BreederX, BreederY)
        elif sample == '轻型飞船':
            LSX = [0 , 0 , 1 , 1 , 1 , 2 , 2 , 2 , 3 , 3 , 3 , 4 ]
            LSY = [20, 21, 19, 20, 21, 19, 20, 22, 20, 21, 22, 21]
            self.set_cell(LSX, LSY)
        elif sample == '轻型飞船+吞噬者':
            EaterX = [0 , 0 , 1 , 1 , 1 , 2 , 2 , 2 , 3 , 3 , 3 , 4 , 35, 35, 36, 37, 37, 37, 38]
            EaterY = [20, 21, 19, 20, 21, 19, 20, 22, 20, 21, 22, 21, 20, 21, 20, 21, 22, 23, 23]
            self.set_cell(EaterX, EaterY)
        elif sample == '开关引擎':
            SEX = [17, 18, 18, 20, 20, 21, 21, 22]
            SEY = [19, 18, 20, 18, 21, 20, 21, 21]
            self.set_cell(SEX, SEY)
        elif sample == '脉冲星':
            CPPX = [8 , 8 , 8 , 8 , 9 , 9 , 9 , 9 , 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 15, 15, 15, 15, 15, 15, 16, 16, 16, 16, 16, 16, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 18, 18, 18, 18, 18, 18, 19, 19, 19, 19, 20, 20, 20, 20]
            CPPY = [10, 11, 17, 18, 11, 12, 16, 17, 8 , 11, 13, 15, 17, 20, 8 , 9 , 10, 12, 13, 15, 16, 18, 19, 20, 9 , 11, 13, 15, 17, 19, 10, 11, 12, 16, 17, 18, 10, 11, 12, 16, 17, 18, 9 , 11, 13, 15, 17, 19, 8 , 9 , 10, 12, 13, 15, 16, 18, 19, 20, 8 , 11, 13, 15, 17, 20, 11, 12, 16, 17, 10, 11, 17, 18]
            self.set_cell(CPPX, CPPY)
    ##根据预设坐标自动键入细胞,并显示棋盘
    def set_cell(self, ListX, ListY):
        for x,y in zip(ListX, ListY):
            self.board1[str(x)][y] = '*'
        self.show_game()

    #显示棋盘
    def show_game(self):
        self.game_GoL.delete('all') ##及时删除之前的画布以防止内存溢出
        self.cell_size = self.game_size / self.size
        for i in range(self.size):
            for j in range(self.size):
                if self.board1[str(i)][j] == '*':
                    self.game_GoL.create_rectangle(self.cell_size*i, self.cell_size*j, self.cell_size*(i+1), self.cell_size*(j+1), fill='white')
                else:
                    self.game_GoL.create_rectangle(self.cell_size*i, self.cell_size*j, self.cell_size*(i+1), self.cell_size*(j+1), fill='black')

if __name__ == "__main__":
    game = Game_of_Life()
    game.set_GoL()