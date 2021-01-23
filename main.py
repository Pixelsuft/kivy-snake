from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.text import Label as CoreLabel
from kivy.graphics import (Color, Ellipse, Rectangle, Line)
from time import sleep as time_sleep
from random import randint as random_int
from os import access as file_exists
from os import F_OK as file_exists_param


class SnakeWidget(Widget):
    fps=60
    default_fps=2
    score=0
    position='menu'
    w, h=Window.size
    w=int(w)
    h=int(h)
    snake=[[5, 2], [4, 2], [3, 2]]
    grid=15
    apple=[random_int(0, int(w/grid)-1), random_int(0, int(h/grid)-1)]
    score=0
    snake_vector='right'
    max_speed=25
    menu_color_back=False
    menu_color_count=50
    over_fps=fps
    over_score=score
    
    
    def set_speed(self, vared):
        self.default_fps=vared
    def set_max_speed(self, vared):
        self.max_speed=vared
    def set_grid(self, vared):
        self.grid=vared
    
    
    def __init__(self, **kwargs):
        super(SnakeWidget, self).__init__(**kwargs)
        txt_cfg='self.set_speed(2)\nself.set_max_speed(18)\nself.set_grid(15)'
        if file_exists('config.txt', file_exists_param):
            temp_f=open('config.txt', 'r')
            txt_cfg=temp_f.read()
            temp_f.close()
        else:
            temp_f=open('config.txt', 'w')
            temp_f.write(txt_cfg)
            temp_f.close()
        self.load_config(txt_cfg)
        Clock.schedule_interval(self.main_loop, 1/self.fps)    
    
    
    def game_over(self):
        self.over_fps=self.fps
        self.over_score=self.score
        self.fps=60
        self.position='game_over'
    
    
    def load_config(self, cfg):
        for i in cfg.split('\n'):
            if not i=='':
                eval(str(i))
    
    
    def main_loop(self, sec):
        with self.canvas:
            if self.position=='menu':
                self.canvas.clear()
                if self.menu_color_back==False:
                    if self.menu_color_count<0:
                        self.menu_color_count=50
                        self.menu_color_back=True
                    else:
                        Color(0, 0, 0, 1)
                        Rectangle(size=(143, 30), pos=((self.width/2)-(143/2), (self.height/2)-(30/2)))
                        Color(0, 1, 0, 1)
                        lab1 = CoreLabel(text="Tap To Start!", font_size=25, color=(0, 1, 0, 1))
                        lab1.refresh()
                        Rectangle(texture=lab1.texture, size=(143, 30), pos=((self.width/2)-(143/2), (self.height/2)-(30/2)))
                        self.menu_color_count-=1
                else:
                    if self.menu_color_count<0:
                        self.menu_color_count=50
                        self.menu_color_back=False
                    else:
                        Color(0, 1, 0, 1)
                        Rectangle(size=(143, 30), pos=((self.width/2)-(143/2), (self.height/2)-(30/2)))
                        Color(1, 0, 0, 1)
                        lab2 = CoreLabel(text="Tap To Start!", font_size=25, color=(0, 0, 0, 1))
                        lab2.refresh()
                        Rectangle(texture=lab2.texture, size=(143, 30), pos=((self.width/2)-(143/2), (self.height/2)-(30/2)))
                        self.menu_color_count-=1
            elif self.position=='game_over':
                self.canvas.clear()
                Color(0, 1, 0, 1)
                label1 = CoreLabel(text="Game Over:(", font_size=25, color=(0, 1, 0, 1))
                label1.refresh()
                label1_size=list(label1.size)
                Rectangle(texture=label1.texture, size=label1_size, pos=((self.width/2)-(label1_size[0]/2), (self.height/2)-30+39))
                label2 = CoreLabel(text="Speed: "+str(self.over_score), font_size=25, color=(0, 1, 0, 1))
                label2.refresh()
                label2_size=list(label2.size)
                Rectangle(texture=label2.texture, size=label2_size, pos=((self.width/2)-(label2_size[0]/2), (self.height/2)-60+39))
                label3 = CoreLabel(text="Score: "+str(self.over_fps), font_size=25, color=(0, 1, 0, 1))
                label3.refresh()
                label3_size=list(label3.size)
                Rectangle(texture=label3.texture, size=label3_size, pos=((self.width/2)-(label3_size[0]/2), (self.height/2)-90+39))
            elif self.position=='game':
                self.canvas.clear()
                Color(0, 1, 0, 1)
                lab_score = CoreLabel(text="Score: "+str(self.score), font_size=25, color=(0, 1, 0, 1))
                lab_score.refresh()
                Rectangle(texture=lab_score.texture, size=list(lab_score.size), pos=(5, self.height-35))
                no_delete=False
                for i in range(len(self.snake)):
                    j=len(self.snake)-1
                    if not j==0:
                        self.snake[j][0]=self.snake[j-1][0]
                        self.snake[j][1]=self.snake[j-1][1]
                if self.snake[0][0]==self.apple[0] and self.snake[0][1]==self.apple[1]:
                    no_delete=True
                    self.score+=1
                    self.apple=[random_int(0, int(self.w/self.grid)-1), random_int(0, int(self.h/self.grid)-1)]
                    if self.fps<=self.max_speed:
                        Clock.unschedule(self.main_loop)
                        self.fps+=random_int(0,2)
                        Clock.schedule_interval(self.main_loop, 1/self.fps)
                if self.snake_vector=='left':
                    if self.snake[0][0]>0:
                        if no_delete==False:
                            self.snake.remove(self.snake[len(self.snake)-1])
                        self.snake.insert(0, [self.snake[0][0]-1,self.snake[0][1]])
                    else:
                        self.game_over()
                elif self.snake_vector=='right':
                    if self.snake[0][0]<self.width/self.grid:
                        if no_delete==False:
                            self.snake.remove(self.snake[len(self.snake)-1])
                        self.snake.insert(0, [self.snake[0][0]+1,self.snake[0][1]])     
                    else:
                        self.game_over()      
                elif self.snake_vector=='down':
                    if self.snake[0][1]>0:
                        if no_delete==False:
                            self.snake.remove(self.snake[len(self.snake)-1])
                        self.snake.insert(0, [self.snake[0][0],self.snake[0][1]-1])    
                    else:
                        self.game_over()  
                elif self.snake_vector=='up':
                    if self.snake[0][1]<self.height/self.grid:
                        if no_delete==False:
                            self.snake.remove(self.snake[len(self.snake)-1])
                        self.snake.insert(0, [self.snake[0][0],self.snake[0][1]+1])
                    else:
                        self.game_over()
                for i in range(len(self.snake)):
                    if int(self.snake[0][0])==int(self.snake[i][0]) and int(self.snake[0][1]==self.snake[i][1]) and not i==0:
                        self.game_over()
                for i in range(len(self.snake)):
                    if i==0:
                        Color(1, 0, 0, 1)
                        Rectangle(pos=(self.snake[i][0]*self.grid, self.snake[i][1]*self.grid), size=(self.grid, self.grid))
                    else:
                        Color(0, 1, 0, 1)
                        Rectangle(pos=(self.snake[i][0]*self.grid, self.snake[i][1]*self.grid), size=(self.grid, self.grid))
                Color(1, 0, 0, 1)
                Rectangle(pos=(self.apple[0]*self.grid, self.apple[1]*self.grid), size=(self.grid, self.grid))
    
    
    def on_touch_down(self, touch):
        if self.position=='menu' or self.position=='game_over':
            Clock.unschedule(self.main_loop)
            self.score=0
            self.position='menu'
            self.w, self.h=Window.size
            self.w=int(self.w)
            self.h=int(self.h)
            self.snake=[[5, 2], [4, 2], [3, 2]]
            self.apple=[random_int(0, int(self.w/self.grid)-1), random_int(0, int(self.h/self.grid)-1)]
            self.score=0
            self.snake_vector='right'
            self.fps=self.default_fps
            self.position='game'
            Clock.schedule_interval(self.main_loop, 1/self.fps)
        elif self.position=='game':
            ws = touch.x / self.size[0]
            hs = touch.y / self.size[1]
            aws = 1 - ws
            if ws > hs and aws > hs:
                if not self.snake_vector=='up':
                    self.snake_vector = 'down'
            elif ws > hs >= aws:
                if not self.snake_vector=='left':
                    self.snake_vector = 'right'
            elif ws <= hs < aws:
                if not self.snake_vector=='right':
                    self.snake_vector = 'left'
            else:
                if not self.snake_vector=='down':
                    self.snake_vector = 'up'
                

class SnakeApp(App):
    def build(self):
        return SnakeWidget()


if __name__=='__main__':
    SnakeApp().run()