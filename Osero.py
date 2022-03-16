
from math import gamma
from os import abort
import numpy as np
import shutil

def wmin(x,y):
    if x > y:
        return y
    else :
        return x
    
terminal_size = shutil.get_terminal_size()
def canPut(gamemap , x, y,player):#0 => おける 1=>おけない
    rangeX = len(gamemap)
    rangeY = len(gamemap[0])
    status = 0 
    #range check
    if x < 0 or x > rangeX-1:
         return 1
    if y < 0 or y > rangeY-1:
         return 1
    
    if gamemap[x][y] != 0 : #is already empty?
         return 1
    #around check
    around_check_status = 0 # 1 is OK ,0 is not ok
    if player == 1:
        if x+1 != rangeX and y != 0:
            if gamemap[x+1][y-1]==2:around_check_status = 1
        if x+1 != rangeX and y+1 != rangeY:
            if gamemap[x+1][y+1] == 2:around_check_status = 1
        if x != 0 and y+1 != rangeY:
            if gamemap[x-1][y+1] == 2 :around_check_status = 1
        if x != 0 and y!=0:
            if gamemap[x-1][y-1] == 2 :around_check_status = 1
        if  y != 0 :
            if gamemap[x][y-1] == 2 :around_check_status = 1
        if y+1 != rangeY :
            if gamemap[x][y+1] == 2 :around_check_status = 1
        if x != 0 :
            if gamemap[x-1][y] == 2 :around_check_status = 1
        if x +1 != rangeX :
            if gamemap[x+1][y] == 2 :around_check_status = 1
    elif player ==2:
        if x+1 != rangeX and y != 0:
            if gamemap[x+1][y-1] == 1: around_check_status = 1
        if x+1 != rangeX and y+1 != rangeY:
            if gamemap[x+1][y+1] == 1: around_check_status = 1
        if x != 0 and y+1 != rangeY:
            if gamemap[x-1][y+1] == 1:around_check_status = 1
        if x != 0 and y != 0:
            if gamemap[x-1][y-1] == 1 : around_check_status = 1
        if  y != 0 :
            if gamemap[x][y-1] == 1 : around_check_status = 1
        if y+1 != rangeY :
            if gamemap[x][y+1] == 1 : around_check_status = 1
        if x != 0 :
            if gamemap[x-1][y] == 1 : around_check_status = 1
        if x+1 != rangeX :
            if gamemap[x+1][y] == 1 : around_check_status = 1
    if around_check_status == 0:
         return 1 #周りになにもないとき
    a_up = look_up(gamemap,x,y)
    a_down = look_down(gamemap,x,y)
    a_right = look_right(gamemap,x,y)
    a_left = look_left(gamemap , x ,y )
    a_right_up = look_right_up(gamemap,x,y)
    a_right_down = look_right_down(gamemap,x,y)
    a_left_up = look_left_up(gamemap,x,y)
    a_left_down = look_left_down(gamemap,x,y)
    
    arounds = [a_up,a_down,a_right,a_left,a_right_up,a_right_down,a_left_down,a_left_up]
    
    a_go_check = 0 #0 == no  1 == OK 2 == skip
    if player == 1:
        for i in range(len(arounds)):      
            a_go_check = 0 
            for j in range(len(arounds[i])-1):
                if a_go_check ==2:
                    continue
                if int(arounds[i][j+1]) == 2:
                    continue;
                elif int(arounds[i][j+1]) == 1:
                    if j != 0:
                        return 0
                    else :a_go_check = 2
                elif arounds[i][j+1] == 0:
                    a_go_check = 2
                    continue
    elif player == 2:
        for i in range(len(arounds)):      
            a_go_check = 0 
            for j in range(len(arounds[i])-1):
                if a_go_check ==2:
                    continue
                if int(arounds[i][j+1]) == 1:
                    continue;
                elif int(arounds[i][j+1]) == 2:
                    if j != 0:
                        return 0
                    else :a_go_check = 2
                elif arounds[i][j+1] == 0:
                    a_go_check = 2
                    continue
    #around check end
    if a_go_check == 1:
        return 0
    else :
        return 1
    


def look_up(gamemap,x,y):
    res = list(range(int(y+1)))
    for i in range(y+1):
        res[i] = gamemap[x][i];
    res.reverse()
    #print(f"x : {x}  y : {y} look_up() : {res}")
    return res;
def look_down(gamemap,x,y):
    rangeY =len(gamemap[0])
    res = list(range(rangeY-y))
    for i in range(rangeY-y):
        res[i] = gamemap[x][i+y]
    #print(f"x : {x}  y : {y}  look_down() : {res}")
    return res
def look_right(gamemap,x,y):
    rangeX = len(gamemap)
    res = list(range(rangeX-x))
    for i in range(rangeX-x):
        res[i] = gamemap[x+i][y]
    #print(f"x : {x} y : {y} look_right() : {res}")
    return res
def look_left(gamemap,x,y):
    res = list(range(x+1))
    for i in range(x+1):
        res[i] = gamemap[i][y]
    res.reverse()
        #print(f"x : {x} y : {y} look_left() : {res}")
    return res
def look_right_up(gamemap,x,y):
    rangeX = len(gamemap)
    res = list(range(wmin(y+1,rangeX-x)))
    for i in range(len(res)):
        res[i] = gamemap[x+i][y-i]
    #print(f"x : {x} y : {y} look_right_up() : {res}")
    return res
def look_right_down(gamemap ,x ,y):
    rangeX = len(gamemap)
    res = list(range(wmin(rangeX-x,len(gamemap[0])-y)))
    for i in range(len(res)):
        res[i] = gamemap[x+i][y+i]
    #print(f"x : {x} y : {y} look_right_down() : {res}")
    return res
def look_left_up(gamemap , x ,y):
    res = list(range(wmin(x+1,y+1)))
    for i in range(len(res)):
        res[i] = gamemap[i-1][len(gamemap[i])-1 -i]
    res.reverse()
    #print(f"x : {x} y : {y} look_left_up() : {res}")
    return res
def look_left_down(gamemap , x, y):
    res = list(range(wmin(x+1,len(gamemap[0])-y)))
    for i in range(len(res)):
        res[i] = gamemap[len(gamemap)-1-i][i]
    res.reverse()
    #print(f"x : {x} y : {y} look_left_down() : {res}")
    return res

def changeStones(gamemap,x,y,turn):
    a_up = look_up(gamemap,x,y)
    a_down = look_down(gamemap,x,y)
    a_right = look_right(gamemap,x,y)
    a_left = look_left(gamemap , x ,y )
    a_right_up = look_right_up(gamemap,x,y)
    a_right_down = look_right_down(gamemap,x,y)
    a_left_up = look_left_up(gamemap,x,y)
    a_left_down = look_left_down(gamemap,x,y)
    arounds = {
                "up":a_up,
                "right_up":a_right_up,
                "right":a_right,
                "right_down":a_right_down,
                "down":a_down,
                "left_down":a_left_down,
                "left":a_left,
                "left_up":a_left_up
               }
    print(arounds)
    nextGameMap = gamemap
    a_go_check = 0
    if canPut(gamemap,x,y,turn)==0: 
        if turn == 1:
            for i in range(len(arounds)):  
                print(str(i))    
                a_go_check = 0 
                for j in range(len(arounds[i])-1):
                    if a_go_check ==2:
                        continue
                    if int(arounds[i][j+1]) == 2:
                        continue;
                    elif int(arounds[i][j+1]) == 1:
                        if j != 0:
                            #fill stone
                            print("filling : "+str(i));
                            
                            a_go_check = 2
                        else :a_go_check = 2
                    elif arounds[i][j+1] == 0:
                        a_go_check = 2
                        continue
        elif turn == 2:
            for i in range(len(arounds)):      
                a_go_check = 0 
                for j in range(len(arounds[i])-1):
                    if a_go_check ==2:
                        continue
                    if int(arounds[i][j+1]) == 1:
                        continue;
                    elif int(arounds[i][j+1]) == 2:
                        if j != 0:
                            #fill stone
                            
                            
                            a_go_check = 2
                        else :a_go_check = 2
                    elif arounds[i][j+1] == 0:
                        a_go_check = 2
                        continue
    
        
        
        
def render(gamemap,turn):
    print("\n" * terminal_size.lines)
    red_cnt = 0
    blue_cnt = 0
    for i in range(len(gamemap)):
        for j in range(len(gamemap[i])):
            if gamemap[i][j] == 1:
                red_cnt += 1
            elif gamemap[i][j] == 2:
                blue_cnt += 1
    print(f"{Color.BG_RED}  {Color.BG_DEFAULT}:{red_cnt}  {Color.BG_BLUE}  {Color.BG_DEFAULT}:{blue_cnt}"  )
    if turn == 1:
        print(f"TURN : PLAYER 1 {Color.BG_RED}  {Color.BG_DEFAULT}")
    else:
        print(f"TURN : PLAYER 2 {Color.BG_BLUE}  {Color.BG_DEFAULT}")
    render_cache = ""
    render_cache = f"{Color.BG_WHITE}  "
    for i in range(len(game_map)):
         render_cache +=f"{i} ";
    print(render_cache+f"x {Color.BG_DEFAULT}")
    for i in range(len(game_map)):
        render_cache =f"{Color.BG_WHITE} {i}"
        for j in range(len(game_map[i])):
            if gamemap[i][j] ==CellType.Player1:
                 render_cache += f"{Color.BG_RED}P1{Color.BG_DEFAULT}"
            elif gamemap[i][j] == CellType.Player2:
                 render_cache += f"{Color.BG_BLUE}P2{Color.BG_DEFAULT}"
            elif gamemap[i][j] == CellType.Select:
                 render_cache += f"{Color.BG_CYAN}=={Color.BG_DEFAULT}"
            else :
                if canPut(gamemap,i,j,turn) ==0:
                    render_cache += f"{Color.BG_WHITE}[]{Color.BG_DEFAULT}"
                else :
                    render_cache += f"{Color.BG_BLACK}[]{Color.BG_DEFAULT}"
        print(render_cache+f"{Color.BG_WHITE}  {Color.BG_DEFAULT}")
    render_cache = Color.BG_WHITE+" y  ";
    for i in range(len(gamemap)):render_cache +="  "
    print(render_cache+Color.BG_DEFAULT)
        
#============================
class Color:
	BLACK          = '\033[30m'#文字 黒
	RED            = '\033[31m'#文字 赤
	GREEN          = '\033[32m'#文字 緑
	YELLOW         = '\033[33m'#文字 黄
	BLUE           = '\033[34m'#文字 青
	MAGENTA        = '\033[35m'#文字 マゼンタ
	CYAN           = '\033[36m'#文字 シアン
	WHITE          = '\033[37m'#文字 白
	COLOR_DEFAULT  = '\033[39m'#文字 デフォルト
	BOLD           = '\033[1m' #太字
	UNDERLINE      = '\033[4m' #下線
	INVISIBLE      = '\033[08m'#不可視
	REVERCE        = '\033[07m'#文字と背景の色を反転
	BG_BLACK       = '\033[40m'#背景 黒
	BG_RED         = '\033[41m'#背景 赤
	BG_GREEN       = '\033[42m'#背景 緑
	BG_YELLOW      = '\033[43m'#背景 黄
	BG_BLUE        = '\033[44m'#背景 青
	BG_MAGENTA     = '\033[45m'#背景 マゼンタ
	BG_CYAN        = '\033[46m'#背景 シアン
	BG_WHITE       = '\033[47m'#背景 白
	BG_DEFAULT     = '\033[49m'#背景 デフォルト
	RESET          = '\033[0m'#リセット
#=============================
class CellType:
    Empty   = 0 #なにもない 
    Player1 = 1 #Player1の石おいてる
    Player2 = 2 #Player2の石おいてる
    Select = 3#選択中
class Status:
    Fighting = 0
    End = 0
x = 8
y = 8

game_map = list(range(x*y))
#init game map
game_map = np.zeros((x,y))
game_map[3][3] = 1
game_map[4][4] = 1
game_map[3][4] = 2
game_map[4][3] = 2
#init game map end
#ingame
game_status = Status.Fighting
game_turn = 1;# 1 or 2
game_last_turn_status = 0 ;
# 0 :   no problem
# 1 : cant place stone here error.
while game_status == Status.Fighting:
    render(game_map,game_turn)
    if game_last_turn_status == 1:
        print(f"you cant put stone here ({select_x},{select_y})")
    game_last_turn_status = 0 
    select_y = int(input("x > "))
    select_x = int(input("y > "))
    #can put? 
    check_status = canPut(game_map , select_x, select_y,game_turn)
    if check_status != 0 :
        game_last_turn_status = 1
        continue
    
    #check end
    #put stone
    changeStones(game_map,select_x,select_y,game_turn)
    #次のターンに回す
    if game_turn == 1 :
        game_turn = 2
    else:
        game_turn = 1
#ingame end
