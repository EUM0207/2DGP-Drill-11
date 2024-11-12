import random
import math
import game_framework
import game_world

from pico2d import *

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Walk', 'Dead']


class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombie/"+ name + " (%d)" % i + ".png") for i in range(1, 11)]

    def __init__(self):
        self.x, self.y = random.randint(1600-800, 1600), 150
        self.load_images()
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])

        #2222222222
        self.hp = 2
        self.state = 'Walk'
        self.dead_timer = 0.0


    def update(self):
        #2222222222
        if self.state == 'Dead':
            self.dead_timer += game_framework.frame_time
            self.frame = int((self.dead_timer * 10) % len(Zombie.images['Dead']))
            if self.dead_timer > len(Zombie.images['Dead']) / 10:  # 애니메이션이 끝나면 제거
                game_world.remove_object(self)
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
            self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
            if self.x > 1600:
                self.dir = -1
            elif self.x < 800:
                self.dir = 1
            self.x = clamp(800, self.x, 1600)
        pass


    def draw(self):
        #2222222222
        size = 200 if self.hp == 2 else 100
        if self.state == 'Dead':
            Zombie.images['Dead'][int(self.frame)].draw(self.x, self.y, size, size)  # Dead 애니메이션
        else:
            if self.dir < 0:
                Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, size, size)
            else:
                Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, size, size)

        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        #2222222222
        size_x = 70 if self.hp == 2 else 35
        size_y = 90 if self.hp == 2 else 45
        # fill here
        return self.x -size_x, self.y -size_y, self.x +size_x, self.y +size_y

    #2222222222
    def handle_collision(self, group, other):
        if group == 'ball:zombie' and self.state != 'Dead':
            self.hp -= 1
            if self.hp <= 0:
                print("Zombie killed: Transition to Dead state")
                self.state = 'Dead'  # Dead 상태로 전환
                self.dead_timer = 0  # Dead 애니메이션 타이머 초기화
            else:
                print("Zombie hit: size halved")