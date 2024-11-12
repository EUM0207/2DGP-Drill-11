from pico2d import *
import game_world
import game_framework

class Ball:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y, self.velocity = x, y, velocity
        #2222222222
        self.on_ground = False

    def draw(self):
        self.image.draw(self.x, self.y)
        #충돌 영역 그리기
        draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.velocity * 100 * game_framework.frame_time

        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)
        #2222222222
        elif self.y <= 30:
            self.on_ground = True


    def get_bb(self):
        # fill here
        return self.x-10, self.y-10, self.x+10, self.y+10

    def handle_collision(self, group, other):
        # fill here
        if group == 'boy:ball' and self.on_ground:
            print("Ball collected by boy")
            game_world.remove_object(self)
        #2222222222
        if group == 'ball:zombie' and not self.on_ground:
            print("Ball hit zombie!")
            game_world.remove_object(self)