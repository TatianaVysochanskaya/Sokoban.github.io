from tkinter import *
from tkinter import ttk
from tkinter import font

import inspect

row_beg = -1
col_beg = -1
row_count = 20            
col_count = 20
man_row = 0                 
man_col = 0

cell_size = 30              
canv_width = cell_size * col_count        
canv_height = cell_size * row_count

cells = []                  

fon_color = "lightgray"
colors = [fon_color, "yellow", "blue", "darkviolet", "red", "green", "chocolate"]


def print_funcname():
    print(inspect.stack()[1][3])


def make_fragm(color_num, row_num, col_num):
    global cells

    cells[row_num][col_num][0] = color_num
    color = colors[ color_num]   
    rect = cells[row_num][col_num][1]
    if color_num in [1,2,3,4,6]:
        bg_color = fon_color
    else:
        bg_color = color
    canv.itemconfig(rect, fill = color, outline = bg_color)



def read_cells():
    global man_row, man_col
    lst_loc = list( fh.read(400) )
    for num in range(400):
        row_num = num // 20
        col_num = num % 20
        color_num = lst_loc[num]
        make_fragm(color_num, row_num, col_num)
        if color_num == 4:
            man_row = row_num
            man_col = col_num
    man_colornum = cells[man_row][man_col][0]        
    #print(man_colornum, man_row, man_col)
    

def move_man(step_row, step_col):
    global cells, man_row, man_col

    man_colornum = cells[man_row][man_col][0]
   
    new_row = man_row + step_row
    new_col = man_col + step_col
    new_colornum = cells[new_row][new_col][0]
    
  
    if new_colornum == 5:
        return 0

    
    if  new_colornum in [2,3]:
        next_row = new_row + step_row
        next_col = new_col + step_col
        next_colornum = cells[next_row][next_col][0]
        if next_colornum in[2,3,5]:  
            return 0
        if man_colornum == 4:
            color_num = 0
        else:
            color_num = 1
        make_fragm(color_num, man_row, man_col)
        if new_colornum == 2:
            man_colornum = 4
        else:    
            man_colornum = 6
        man_row = new_row
        man_col = new_col
        make_fragm(man_colornum, man_row, man_col)

        
        if next_colornum == 0:
            color_num = 2
        else:
            color_num = 3
        make_fragm(color_num, next_row, next_col)

        return 1

    if man_colornum == 4:
        color_num = 0
    else:
        color_num = 1
    make_fragm(color_num, man_row, man_col)
    
    
    if new_colornum == 0:
        man_colornum = 4
    elif new_colornum == 1:    
        man_colornum = 6
    man_row = new_row
    man_col = new_col
    make_fragm(man_colornum, man_row, man_col)
    return 1


root = Tk()
stl = ttk.Style()
clr_root = "lime"
dFont = font.Font(family="helvetica", size=14)
stl.configure('.', font=dFont, background=clr_root, foreground= "black")

btn_width = 8             
pnl_top = Frame(root)
pnl_top.grid(row = 2, column = 0, columnspan = 10)

canv = Canvas(pnl_top, width = canv_width, height = canv_height, background = fon_color )
canv.pack()


def fnc_load():
    level_num = var_level.get()
    if level_num < 1:
        level_num = 1
        
    if level_num >=  level_count:
        level_num =  level_count

    var_level.set(level_num)

    
    fh.seek( 400*(level_num-1) )
    read_cells()
    
btn_load = ttk.Button( root, text = "load", width = btn_width, command = fnc_load)
btn_load.grid(row = 1, column = 0, sticky=E+N, pady = 5 , padx = 5)

var_level = IntVar()
var_level.set(1)

edt_level = ttk.Entry(root, width = 5, textvariable= var_level, justify = RIGHT, font = dFont )
edt_level.grid(row = 1, column = 1, padx= 5, pady = 5)



for row_num in range(row_count):
    row = []
    for col_num in range(col_count):
        x_beg = col_num * cell_size;  x_end = x_beg + cell_size
        y_beg = row_num * cell_size;  y_end = y_beg + cell_size
        rect = canv.create_rectangle(x_beg+1, y_beg+1, x_end-1, y_end-1, fill = fon_color, outline = fon_color, width = 2 )
        row.append([0,rect])
    cells.append(row)


file_name = "sokoban.bin"
fh = open( file_name, "rb+")
level_count = fh.seek(0,2) // 400  


def shift_down( ):          
    res = move_man( 1, 0)


def shift_up( ):            
    res =  move_man( -1, 0)


def shift_right( ):         
    res =  move_man( 0,1)


def shift_left():           
    res =  move_man( 0,-1)

def key_hndl(event):
    global key
    key = event.keysym

    dct_func = {"Left":shift_left, "Right":shift_right,
                "Up":shift_up, "Down":shift_down }
    if not key in dct_func.keys():  
        return

    	
    func = dct_func[key]
    res = func( )
    return

root.bind("<Key>", key_hndl)


root.mainloop()
fh.close()

