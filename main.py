from game import Game
from eventdisp import Dispatcher
import pygame as pg
from player import Player


cols, rows = 25, 25
TILE = 30

pg.init()
sc = pg.display.set_mode([cols * TILE, rows * TILE])
clock = pg.time.Clock()

dispatcher = Dispatcher()

game = Game(dispatcher, cols, rows, TILE)


dispatcher.emmit("change_location")

p = Player(dispatcher)

while True:
    sc.fill(pg.Color('black'))

    if p.x > (cols - 1) * TILE:
        p.x = 0
        dispatcher.emmit('change_location', game.grid)

    if p.x < 0:
        p.x = ((cols - 1) * TILE) - 1
        dispatcher.emmit('change_location', game.grid)

    if p.y > (rows - 1) * TILE:
        p.y = 0
        dispatcher.emmit('change_location', game.grid)

    if p.y < 0:
        p.y = ((rows - 1) * TILE) - 1
        dispatcher.emmit('change_location', game.grid)

    [[pg.draw.rect(sc, pg.Color('darkorange'), game.get_rect(x, y), border_radius=TILE // 5)
      for x, col in enumerate(row) if col] for y, row in enumerate(game.grid)]

    pg.draw.rect(sc, p.color, (p.x, p.y, TILE//2, TILE//2), border_radius=TILE // 5)
    pg.draw.rect(sc, pg.Color('green'), game.food, border_radius=TILE // 5)

    font = pg.font.Font(None, 50)
    text = font.render(str(game.score), True, (100, 255, 100))
    # text = font.render(str(p.vel_x), True, (100, 255, 100))
    text_x = cols * TILE // 2 - text.get_width() // 2
    text_y = text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    sc.blit(text, (text_x, text_y))

    if game.check_collisions(p):
        dispatcher.emmit('player_change_color')
        dispatcher.emmit('change_score', -10)
        dispatcher.emmit('player_bounsing_off', p)

    if game.check_food(p):
        dispatcher.emmit('change_score', 500)
        dispatcher.emmit('player_change_color')
        dispatcher.emmit('eat_food')

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

    keys = pg.key.get_pressed()

    if keys[pg.K_RIGHT]:
        if p.vel_x < 10:
            p.vel_x += 0.1
    elif keys[pg.K_LEFT]:
        if p.vel_x > -10:
            p.vel_x -= 0.1
    elif keys[pg.K_UP]:
        if p.vel_y < 10:
            p.vel_y -= 0.1
    elif keys[pg.K_DOWN]:
        if p.vel_y > -10:
            p.vel_y += 0.1

    if keys[pg.K_RIGHT] or keys[pg.K_LEFT] or keys[pg.K_UP] or keys[pg.K_DOWN]:
        pass
    else:
        if abs(p.vel_x) > 0.2:
            p.vel_x = p.vel_x - (0.1 * (p.vel_x / abs(p.vel_x)))
        else:
            p.vel_x = 0

        if abs(p.vel_y) > 0.2:
            p.vel_y = p.vel_y - (0.1 * (p.vel_y / abs(p.vel_y)))
        else:
            p.vel_y = 0

    p.vel_x = min(20, p.vel_x)
    p.vel_y = min(20, p.vel_y)
    p.move()

    pg.display.flip()
    clock.tick(60)
