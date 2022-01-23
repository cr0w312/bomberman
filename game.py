from random import random, randrange


class Game:

    def __init__(self, dispatcher, cols, rows, tile):
        self.cols = cols
        self.rows = rows
        self.tile = tile
        self.food = (0, 0, tile, tile)
        self.grid = []
        self.score = 0
        dispatcher.add_listener("change_score", self.change_score)
        dispatcher.add_listener("change_location", self.change_location)
        dispatcher.add_listener("eat_food", self.eat_food)
        dispatcher.add_listener('player_bounsing_off', self.bounse)

    def change_score(self, param=0):
        self.score += param
        print(self.score)

    def get_rect(self, x, y):
        return x * self.tile + 1, y * self.tile + 1, self.tile - 2, self.tile - 2

    def change_location(self, param=0):
        self.grid = [[1 if random() < 0.2 else 0 for col in range(self.cols)] for row in range(self.rows)]
        self.food = (randrange(0, self.cols * self.tile), randrange(0, self.rows * self.tile), self.tile, self.tile)

    def bounse(self, p):
        if p.vel_x != 0:
            p.vel_x = -p.vel_x // 2 - (p.vel_x // abs(p.vel_x))
            
        if p.vel_y != 0:
            p.vel_y = -p.vel_y // 2 - (p.vel_y // abs(p.vel_y))
            

    def eat_food(self, param=0):
        self.food = (-100, -100, 0, 0)

    def check_food(self, player):
        if (player.x + (self.tile // 2) > self.food[0]) \
                and player.x < self.food[0] + self.tile \
                and (player.y + (self.tile // 2)) > self.food[1] \
                and (player.y < self.food[1] + self.tile):
            return True
        return False

    def check_collisions(self, player):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == 1:
                    wall_x = col * self.tile
                    wall_y = row * self.tile
                    if ((player.x + self.tile // 2) > wall_x) \
                            and (player.x < wall_x + self.tile) \
                            and ((player.y + self.tile // 2) > wall_y) \
                            and (player.y < wall_y + self.tile):
                        return True
        return False
