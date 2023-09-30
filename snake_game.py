#simple snake game using python 3 for beginners
#@codealpha 

from tkinter import *
import random
from tkinter import messagebox
from tkinter import simpledialog
'''
CONSTANTS
'''
WIDTH=600
HEIGHT=600
SPACE_SIZE=30
BODY= 4 # body parts of snake
SNAKE_COLOR="#00FF00"
FOOD_COLOR="#FF0000"
BACKGROUND_COLOR="#000000"
'''
Variables
'''
score=0
speed= 60
direction='right'
player_name=""
'''
CLASSES
'''
class Snake():
    def __init__(self):
        self.body_size=BODY
        self.coordinates=[]
        self.squares=[]
        for i in range(0,BODY):
            self.coordinates.append([0,0])
        for x ,y in self.coordinates:
            square=canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=SNAKE_COLOR,tag='snake')
            self.squares.append(square)



class Food:
    def __init__(self):
        x=(random.randint(0,(WIDTH/SPACE_SIZE)-1)*SPACE_SIZE)
        y=(random.randint(0,(HEIGHT/SPACE_SIZE)-1))*SPACE_SIZE
        self.coordinates=[x,y]
        canvas.create_oval(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=FOOD_COLOR,tag='food') # starting and ending corrdinates
'''
FUNCTIONS
'''
def start_game(player_name):
    global score, direction,speed
    score = 0
    speed=50
    direction = 'right'  # Reset the direction
    label.config(text="Player: {}\nScore: {}".format(player_name, score))
    canvas.delete("game")  # Clear the "Game Over" message
    snake = Snake()
    food = Food()
    next_move(snake, food)

def is_collided(snake:Snake)->bool:
    global score
    x,y=snake.coordinates[0]
    if x<0 or x>=WIDTH:
        return True
    elif y<0 or y>=HEIGHT:
        return True
    for body in snake.coordinates[1:]:
        if x==body[0] and y==body[1]:
            return True
    return False
def game_over(player_name):
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('arial', 50), text='Game Over!', fill='red', tag='game')
    replay = messagebox.askyesno("Game Over", "Play again?")
    if replay:
        start_game(player_name)
    else:
        window.quit()

def on_start():
    global player_name
    player_name = simpledialog.askstring("Player Name", "Enter your name:")
    if player_name:
        start_game(player_name)

def next_move(snake,food):
    global speed,player_name,score
    x,y=snake.coordinates[0]
    if direction=='up':
        y-=SPACE_SIZE
    elif direction=='down':
        y+=SPACE_SIZE
    elif direction == 'left':
        x-=SPACE_SIZE
    elif direction == 'right':
        x+=SPACE_SIZE
    snake.coordinates.insert(0,(x,y))
    square=canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=SNAKE_COLOR)
    snake.squares.insert(0,square)
    if x==food.coordinates[0] and y==food.coordinates[1]:
        score+=1
        label.config(text="Player: {}\nScore: {}".format(player_name, score))
        canvas.delete('food')
        food = Food()
        if speed > 5:
            speed -= 1

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    if is_collided(snake):
        game_over(player_name=player_name)
    else:
        window.after(speed,next_move,snake,food)

def change_direction(direction_new):
    global direction
    if direction_new=='left':
        if direction!='right':
            direction=direction_new
    elif direction_new=='up':
        if direction!='down':
            direction=direction_new
    elif direction_new=='right':
        if direction!='left':
            direction=direction_new
    elif direction_new=='down':
        if direction!='up':
            direction=direction_new
'''
TKINTER
'''
window=Tk()
window.title('Classic Snake Game')
window.resizable(False,False)
label=Label(window,text='Score: {}'.format(score),font=('arial',20))
label.pack()
canvas=Canvas(window,background=BACKGROUND_COLOR,height=HEIGHT,width=WIDTH)
canvas.pack()
window.update()
window_w=window.winfo_width()
window_h=window.winfo_height()
screen_w=window.winfo_screenwidth()
screen_h=window.winfo_screenheight()

x=int((screen_w/2)-(window_w/2))
y=int((screen_h/2)-(window_h/2))

window.geometry(f'{window_w}x{window_h}+{x}+{y}')
window.bind('<Left>',lambda x: change_direction('left'))
window.bind('<Right>',lambda x: change_direction('right'))
window.bind('<Up>',lambda x: change_direction('up'))
window.bind('<Down>',lambda x: change_direction('down'))

start_button = Button(window, text="Start", command=on_start)
start_button.pack()
on_start()



window.mainloop()