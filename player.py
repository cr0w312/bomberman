import pygame as pg
from random import randrange


class Player:
    def __init__(self, event_mgr):
        self.x = 0
        self.y = 0
        self.color = pg.Color('blue')
        self.vel_x = 0
        self.vel_y = 0
        event_mgr.add_listener('player_change_color', self.change_color)

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def change_color(self, param):
        self.color = pg.Color(randrange(1, 200), randrange(1, 200), randrange(1, 200))