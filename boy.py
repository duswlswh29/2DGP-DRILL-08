from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT,SDLK_a


from state_machine import StateMachine

def space_down(e):
    return e[0]=='INPUT' and e[1].type==SDL_KEYDOWN and e[1].key==SDLK_SPACE

def time_out(e):
    return e[0]=='TIME_OUT'

def right_down(e):
    return e[0]=='INPUT' and e[1].type==SDL_KEYDOWN and e[1].key==SDLK_RIGHT

def left_down(e):
    return e[0]=='INPUT' and e[1].type==SDL_KEYDOWN and e[1].key==SDLK_LEFT

def right_up(e):
    return e[0]=='INPUT' and e[1].type==SDL_KEYUP and e[1].key==SDLK_RIGHT

def left_up(e):
    return e[0]=='INPUT' and e[1].type==SDL_KEYUP and e[1].key==SDLK_LEFT #수정

def autorun_a_down(e):
    return e[0]=='INPUT' and e[1].type==SDL_KEYDOWN and e[1].key==SDLK_a

class AutoRun:

    def __init__(self, boy):
        self.boy = boy

    def enter(self,e):
        self.boy.dir = self.boy.face_dir #방향 1에서 수정

        self.boy.wait_start_time=get_time()

    def exit(self,e):
        pass

    def do(self): #2초 이상되면 SLEEP
        self.boy.frame = (self.boy.frame + 1) % 8
        self.boy.x+=self.boy.dir*10#속도 빠름
        if get_time() - self.boy.wait_start_time> 5 :
            self.boy.state_machine.handle_state_event(('TIME_OUT',None))

        if self.boy.x>780:
            self.boy.x=780
            self.boy.dir=-1
            self.boy.face_dir=-1 #자동 방향반전

        elif self.boy.x<20:
            self.boy.x=20
            self.boy.dir=1
            self.boy.face_dir=1



    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_draw(self.boy.frame * 100, 100, 100, 100, self.boy.x, self.boy.y+10,150,150)
        else: # face_dir == -1: # left
            self.boy.image.clip_draw(self.boy.frame * 100, 0, 100, 100, self.boy.x, self.boy.y+10,150,150)


class Run:  #right down이아니라 left up일때도 발생할 수 잇다 동시입략?

    def __init__(self, boy):
        self.boy = boy

    def enter(self,e):
        if right_down(e) or left_up(e):
            self.boy.dir=self.boy.face_dir=1
        elif left_down(e) or right_up(e):
            self.boy.dir=self.boy.face_dir=-1
    def exit(self,e):
        pass

    def do(self): #2초 이상되면 SLEEP
        self.boy.frame = (self.boy.frame + 1) % 8
        self.boy.x+=self.boy.dir*5

        if self.boy.x>780:
            self.boy.x=780
        elif self.boy.x<20:
            self.boy.x=20





    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_draw(self.boy.frame * 100, 100, 100, 100, self.boy.x, self.boy.y)
        else: # face_dir == -1: # left
            self.boy.image.clip_draw(self.boy.frame * 100, 0, 100, 100, self.boy.x, self.boy.y)


class Sleep:

    def __init__(self, boy):
        self.boy = boy

    def enter(self,e):
        self.boy.dir = 0

    def exit(self,e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8

    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_composite_draw(self.boy.frame * 100, 300, 100, 100, 3.141592/2,'',self.boy.x, self.boy.y-30,100,100)
        else: # face_dir == -1: # left
            self.boy.image.clip_composite_draw(self.boy.frame * 100, 200, 100, 100, -3.141592/2,'',self.boy.x, self.boy.y-30,100,100)


class Idle:

    def __init__(self, boy):
        self.boy = boy

    def enter(self,e):
        self.boy.dir = 0
        self.boy.wait_start_time=get_time()

    def exit(self,e):
        pass

    def do(self): #2초 이상되면 SLEEP
        self.boy.frame = (self.boy.frame + 1) % 8
        if get_time() - self.boy.wait_start_time> 2.5:
            self.boy.state_machine.handle_state_event(('TIME_OUT',None))

            #이게 그래서 2초 하고 프로그램이 죽어버리나? 음.. 아니면 그냥 sleep?



    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_draw(self.boy.frame * 100, 300, 100, 100, self.boy.x, self.boy.y)
        else: # face_dir == -1: # left
            self.boy.image.clip_draw(self.boy.frame * 100, 200, 100, 100, self.boy.x, self.boy.y)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('animation_sheet.png')

        self.IDLE = Idle(self)
        self.SLEEP = Sleep(self)
        self.RUN = Run(self)
        self.AUTORUN=AutoRun(self)
        self.state_machine = StateMachine(
        self.IDLE,{ #시작상태
            self.SLEEP: {space_down:self.IDLE,right_down:self.RUN,left_down:self.RUN},
            self.IDLE:{right_down:self.RUN, left_down:self.RUN,left_up:self.IDLE, right_up:self.IDLE,time_out:self.SLEEP,autorun_a_down:self.AUTORUN},
            self.RUN: {right_down:self.RUN,left_down:self.RUN,right_up:self.IDLE, left_up:self.IDLE},
            self.AUTORUN:{right_down:self.RUN,left_down:self.RUN,time_out:self.IDLE}

        }
        )

    def update(self):
        self.state_machine.update()


    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT',event))#처리히리고 넘겨줌

    pass