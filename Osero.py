from math import gamma
from os import abort
import numpy as np
import shutil

def wmin(x,y):
    if x > y:
        return y
    else :
        return x
def get_var_name(var):
    for k,v in globals().items():
        if id(v) == id(var):
            name=k
    return name
                
class Direction:
    UP           = 0
    RIGHT_UP     = 1
    RIGHT        = 2
    RIGHT_DOWN   = 3
    DOWN         = 4
    LEFT_DOWN    = 5
    LEFT         = 6
    LEFT_UP      = 7
class CellType:
    Empty   = 0 #なにもない 
    Player1 = 1 #Player1の石おいてる
    Player2 = 2 #Player2の石おいてる
    Select = 3#選択中   
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
    #print(f"x:{x} y:{y} {a_left_up}")
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
    


def look_left(gamemap,x,y):
    res = list(range(int(y+1)))
    for i in range(y+1):
        res[i] = gamemap[x][i];
    res.reverse()
    #print(f"x : {x}  y : {y} look_up() : {res}")
    return res;
def look_right(gamemap,x,y):
    rangeY =len(gamemap[0])
    res = list(range(rangeY-y))
    for i in range(rangeY-y):
        res[i] = gamemap[x][i+y]
    #print(f"x : {x}  y : {y}  look_down() : {res}")
    return res
def look_down(gamemap,x,y):
    rangeX = len(gamemap)
    res = list(range(rangeX-x))
    for i in range(rangeX-x):
        res[i] = gamemap[x+i][y]
    #print(f"x : {x} y : {y} look_right() : {res}")
    return res
def look_up(gamemap,x,y):
    res = list(range(x+1))
    for i in range(x+1):
        res[i] = gamemap[i][y]
    res.reverse()
        #print(f"x : {x} y : {y} look_left() : {res}")
    return res
def look_left_down(gamemap,x,y):
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
        res[i] = gamemap[x-i][y-i]
    #print(f"x : {x} y : {y} look_left_up() : {res}")
    return res
def look_right_up(gamemap , x, y):#gamemap[y][x]
    res = list(range(wmin(x+1,len(gamemap[0])-y)))
    for i in range(len(res)):
        if x-i >= 8 :
            break
        if i+y >= len(gamemap[0]):
            break;
        res[i] = gamemap[x-i][y+i]    
    return res

def changeStones(gamemap,x,y,turn):
    print(f"changeStone(x:{x},y:{y}) : ")
    a_up = look_up(gamemap,x,y)
    a_down = look_down(gamemap,x,y)
    a_right = look_right(gamemap,x,y)
    a_left = look_left(gamemap , x ,y )
    a_right_up = look_right_up(gamemap,x,y)
    a_right_down = look_right_down(gamemap,x,y)
    a_left_up = look_left_up(gamemap,x,y)
    a_left_down = look_left_down(gamemap,x,y)
    arounds =[]
    arounds += [a_up,a_right_up,a_right,a_right_down,a_down,a_left_down,a_left,a_left_up]
    # up rightup right rightdown down leftdown left leftup
    for i in range(len(arounds)):
        print(i)
    Direction_to_go = [False,False,False,False,False,False,False,False]
    print(arounds)
    nextGameMap = gamemap
    print(nextGameMap)
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
                            Direction_to_go[i] = True                       
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
                            Direction_to_go[i] = True
                            a_go_check = 2
                        else :a_go_check = 2
                    elif arounds[i][j+1] == 0:
                        a_go_check = 2
                        continue 
        nx = x
        x = y
        y = nx   
        dtg_res = ""
        #print(f"changeStone(x:{x},y:{y}) : ")
        for i in range(len(Direction_to_go)):
            if Direction_to_go[i] ==True:
                if i==Direction.UP:
                    dtg_res +="up,"
                if i==Direction.DOWN:
                    dtg_res+="down,"
                if i==Direction.RIGHT:
                    dtg_res+="right,"
                if i==Direction.LEFT:
                    dtg_res+="left,"
                if i==Direction.RIGHT_UP:
                    dtg_res+="rigth_up,"
                if i==Direction.RIGHT_DOWN:
                    dtg_res +="right_down"
                if i==Direction.LEFT_UP:
                    dtg_res +="left_up"
                if i==Direction.LEFT_DOWN:
                    dtg_res+="left_down"
        print(dtg_res)
        
        if turn == 1:
            for i in range(len(Direction_to_go)):
                if Direction_to_go[i] == True:
                    if i == Direction.UP :
                        nextGameMap[y][x] = CellType.Player1
                        for j in range(len(arounds[i])-1):
                            #print(nextGameMap[x][y-j])
                            if j == 0 :
                                #print("continue")
                                continue
                            if nextGameMap[y-j][x] == CellType.Player2:
                                #print("replace")
                                nextGameMap[y-j][x] = CellType.Player1
                                continue
                            if nextGameMap[y-j][x] == CellType.Player1:
                                #print("end")
                                break;
                    if i == Direction.DOWN :
                        nextGameMap[y][x] = CellType.Player1
                        for j in range(len(arounds[i])-2):
                            #print(nextGameMap[x][y+j])
                            if j == 0 :
                                #print("continue")
                                continue
                            if nextGameMap[y+j][x] == CellType.Player2:
                                #print("replace!")
                                nextGameMap[y+j][x] = CellType.Player1
                                continue
                            if nextGameMap[y+j][x] == CellType.Player1:
                                #print("end")
                                break;
                    if i == Direction.RIGHT:#←
                        nextGameMap[y][x] = CellType.Player1
                        for j in range(len(arounds[i])-1):
                            #print(nextGameMap[x][y])
                            if j == 0 :
                                #print("continue")
                                continue
                            if nextGameMap[y][x+j] == CellType.Player2:
                                #print("replace!")
                                nextGameMap[y][x+j] = CellType.Player1
                                continue
                            if nextGameMap[y][x+j] == CellType.Player1:
                                #print("end")
                                break;
                    if i == Direction.LEFT:
                        nextGameMap[y][x] = CellType.Player1
                        for j in range(len(arounds[i])-2):
                            #print(nextGameMap[x][y])
                            if j == 0 :
                                #print("continue")
                                continue
                            if nextGameMap[y][x-j] == CellType.Player2:
                                #print("replace!")
                                nextGameMap[y][x-j] = CellType.Player1
                                continue
                            if nextGameMap[y][x-j] == CellType.Player1:
                                #print("end")
                                break;
                    if i == Direction.RIGHT_UP:
                        nextGameMap[y][x] = CellType.Player1
                        for j in range(len(arounds[i])-1):
                            #print(nextGameMap[x][y])
                            if j == 0 :
                                #print("continue")
                                continue
                            if nextGameMap[y-j][x+j] == CellType.Player2:
                                #print("replace!")
                                nextGameMap[y-j][x+j] = CellType.Player1
                                continue
                            if nextGameMap[y-j][x+j] == CellType.Player1:
                                #print("end")
                                break;
                    if i == Direction.RIGHT_DOWN:
                        nextGameMap[y][x] = CellType.Player1
                        for j in range(len(arounds[i])-1):
                            #print(nextGameMap[x][y])
                            if j == 0 :
                                #print("continue")
                                continue
                            if nextGameMap[y+j][x+j] == CellType.Player2:
                                #print("replace!")
                                nextGameMap[y+j][x+j] = CellType.Player1
                                continue
                            if nextGameMap[y+j][x+j] == CellType.Player1:
                                #print("end")
                                break;
                    if i == Direction.LEFT_DOWN:
                        nextGameMap[y][x] = CellType.Player1
                        for j in range(len(arounds[i])-1):
                            #print(nextGameMap[x][y])
                            if j == 0 :
                                #print("continue")
                                continue
                            if nextGameMap[y+j][x-j] == CellType.Player2:
                                #print("replace!")
                                nextGameMap[y+j][x-j] = CellType.Player1
                                continue
                            if nextGameMap[y+j][x-j] == CellType.Player1:
                                #print("end")
                                break;
                    if i == Direction.LEFT_UP:
                        nextGameMap[y][x] = CellType.Player1
                        for j in range(len(arounds[i])-1):
                            #print(nextGameMap[x][y])
                            if j == 0 :
                                #print("continue")
                                continue
                            if nextGameMap[y-j][x-j] == CellType.Player2:
                                #print("replace!")
                                nextGameMap[y-j][x-j] = CellType.Player1
                                continue
                            if nextGameMap[y-j][x-j] == CellType.Player1:
                                #print("end")
                                break;
        elif turn ==2:
            for i in range(len(Direction_to_go)):
                if Direction_to_go[i] == True:
                    if i == Direction.UP :
                        nextGameMap[y][x] = CellType.Player2
                        for j in range(len(arounds[i])-1):
                            #print(nextGameMap[x][y-j])
                            if j == 0 :
                                #print("continue")
                                continue
                            if nextGameMap[y-j][x] == CellType.Player1:
                                #print("replace")
                                nextGameMap[y-j][x] = CellType.Player2
                                continue
                            if nextGameMap[y-j][x] == CellType.Player2:
                                #print("end")
                                break;
                    if i == Direction.DOWN :
                        nextGameMap[y][x] = CellType.Player2
                        for j in range(len(arounds[i])-2):
                            #print(nextGameMap[x][y+j])
                            if j == 0 :
                                #print("continue")
                                continue
                            if nextGameMap[y+j][x] == CellType.Player1:
                                #print("replace!")
                                nextGameMap[y+j][x] = CellType.Player2
                                continue
                            if nextGameMap[y+j][x] == CellType.Player2:
                                #print("end")
                                break;
                    if i == Direction.RIGHT:#←
                        nextGameMap[y][x] = CellType.Player2
                        for j in range(len(arounds[i])-1):
                            #print(nextGameMap[x][y])
                            if j == 0 :
                                #print("continue")
                                continue
                            if nextGameMap[y][x+j] == CellType.Player1:
                                #print("replace!")
                                nextGameMap[y][x+j] = CellType.Player2
                                continue
                            if nextGameMap[y][x+j] == CellType.Player2:
                                #print("end")
                                break;
                    if i == Direction.LEFT:
                        nextGameMap[y][x] = CellType.Player2
                        for j in range(len(arounds[i])-2):
                            #print(nextGameMap[x][y])
                            if j == 0 :
                                #print("continue")
                                continue
                            if nextGameMap[y][x-j] == CellType.Player1:
                                #print("replace!")
                                nextGameMap[y][x-j] = CellType.Player2
                                continue
                            if nextGameMap[y][x-j] == CellType.Player2:
                                #print("end")
                                break;
                    if i == Direction.RIGHT_UP:
                        nextGameMap[y][x] = CellType.Player2
                        for j in range(len(arounds[i])-1):
                            #print(nextGameMap[x][y])
                            if j == 0 :
                                #print("continue")
                                continue
                            if nextGameMap[y-j][x+j] == CellType.Player1:
                                #print("replace!")
                                nextGameMap[y-j][x+j] = CellType.Player2
                                continue
                            if nextGameMap[y-j][x+j] == CellType.Player2:
                                #print("end")
                                break;
                    if i == Direction.RIGHT_DOWN:
                        nextGameMap[y][x] = CellType.Player2
                        for j in range(len(arounds[i])-1):
                            #print(nextGameMap[x][y])
                            if j == 0 :
                                #print("continue")
                                continue
                            if nextGameMap[y+j][x+j] == CellType.Player1:
                                #print("replace!")
                                nextGameMap[y+j][x+j] = CellType.Player2
                                continue
                            if nextGameMap[y+j][x+j] == CellType.Player2:
                                #print("end")
                                break;
                    if i == Direction.LEFT_DOWN:
                        nextGameMap[y][x] = CellType.Player2
                        for j in range(len(arounds[i])-1):
                            #print(nextGameMap[x][y])
                            if j == 0 :
                                #print("continue")
                                continue
                            if nextGameMap[y+j][x-j] == CellType.Player1:
                                #print("replace!")
                                nextGameMap[y+j][x-j] = CellType.Player2
                                continue
                            if nextGameMap[y+j][x-j] == CellType.Player2:
                                #print("end")
                                break;
                    if i == Direction.LEFT_UP:
                        nextGameMap[y][x] = CellType.Player2
                        for j in range(len(arounds[i])-1):
                            #print(nextGameMap[x][y])
                            if j == 0 :
                                #print("continue")
                                continue
                            if nextGameMap[y-j][x-j] == CellType.Player1:
                                #print("replace!")
                                nextGameMap[y-j][x-j] = CellType.Player2
                                continue
                            if nextGameMap[y-j][x-j] == CellType.Player2:
                                #print("end")
                                break;
        return nextGameMap
                            
    return nextGameMap;
                
def render(gamemap,turn):
    mx_y = len(gamemap[0])
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
        if mx_y > 10 and i < 10:
            render_cache +=" "
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
    #ゲーム終了チェック
    game_player1_cnt = 0
    game_player2_cnt = 0
    for i in range(len(game_map)):
        for j in range(len(game_map[i])):
            if game_map[i][j] == 1:
                game_player1_cnt += 1
            elif game_map[i][j] == 2:
                game_player2_cnt += 1
    if game_player2_cnt == 0:
        game_status = Status.End
    elif game_player1_cnt == 0:
        game_status = Status.End
        
    if game_status == Status.End:#おわってたら
        render(game_map,game_turn)
        if game_player1_cnt == 0:
            print("player2 win!")
            exit()
        elif game_player2_cnt == 0:
            print("player1 win!")
            exit()

    render(game_map,game_turn)
    if game_last_turn_status == 1:
        print(f"you cant put stone here ({select_x},{select_y})")
    game_last_turn_status = 0 
    if game_status == Status.Fighting:
        select_y = int(input("x > "))
        select_x = int(input("y > "))
        #can put? 
        check_status = canPut(game_map , select_x, select_y,game_turn)
        if check_status != 0 :
            game_last_turn_status = 1
            continue
        
        #check end
        #put stone
        game_map = changeStones(game_map,select_x,select_y,game_turn)
        #次のターンに回す
        if game_turn == 1 :
            game_turn = 2
        else:
            game_turn = 1
#ingame end
