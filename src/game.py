#! /usr/bin/env python3

import pygame
import config
import colors


def continue_game(surface):
    import pickle

    # make sure that we actually have the data if we select this

    with open('../data/saved_data.pckl', 'rb') as f:
        data = pickle.load(f)

    config.data = data

    gameplay(surface)

    return


def quit_game(surface):
    from sys import exit
    import pickle
    import os

    os.makedirs('../data', exist_ok=True)

    with open('../data/saved_data.pckl', 'wb') as f:
        pickle.dump(f, config.data, protocol=-1)

    pygame.quit()
    exit()

    return


def gameplay(surface):

    data = config.data

    tower_img = pygame.image.load('../assets/tiles/tower/wR.bmp').convert()
    tower_img.set_colorkey(colors.colorkey)

    wall_tile = pygame.image.load('../assets/tiles/floor/ \
                                   dngn_rock_wall_00.bmp').convert()
    floor_tile = pygame.image.load('../assets/tiles/floor/ \
                                    dngn_floor.bmp').convert()
    path_tile = pygame.image.load('../assets/tiles/floor/ \
                                   dngn_floor_lair.bmp').convert()
    water_tile = pygame.image.load('../assets/tiles/floor/ \
                                    dngn_shallow_water.bmp').convert()
    entrance_tile = pygame.image.load('../assets/tiles/floor/ \
                                       dngn_enter_abyss.bmp').convert()
    exit_tile = pygame.image.load('../assets/tiles/floor/ \
                                   dngn_exit.bmp').convert()

    wall_tile.set_colorkey(colors.colorkey)
    floor_tile.set_colorkey(colors.colorkey)
    path_tile.set_colorkey(colors.colorkey)
    water_tile.set_colorkey(colors.colorkey)
    entrance_tile.set_colorkey(colors.colorkey)
    exit_tile.set_colorkey(colors.colorkey)

    tiles = {'wall': wall_tile,
             'floor': floor_tile,
             'path': path_tile,
             'water': water_tile,
             'entrance': entrance_tile,
             'exit': exit_tile,
             }

    while True:
        surface.fill(colors.black)

        blit_level(surface, tiles, data['level'])

        for tower in data['towers']:
            blit_tower(surface, tower_img, tower)

        blit_score(surface, data['score'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(surface)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                create_tower(event.pos)

        pygame.display.flip()


def blit_level(surface, tiles, level):
    game_map_file = '../assets/maps/map_{}.txt'.format(level)

    # for testing purposes
    game_map_file = '../assets/maps/test.txt'

    game_map = parse_map(game_map_file)

    tile_loc = pygame.Rect(10, 10, 32, 32)

    for row in game_map:
        for tile in row:
            tile_loc = tile_loc.move_ip(32, 0)
            surface.blit(tiles[tile], tile_loc)
        tile_loc.move_ip(-32 * len(row), 32)

    pass


def blit_tower(surface, tower_img, tower):

    tower_loc = tower_img.get_rect(center=(tower.x,
                                           tower.y))

    surface.blit(tower_img, tower_loc)

    return


def blit_score(surface, score):

    font = pygame.font.SysFont(config.fontname, config.fontsize)

    score_rendered = font.render(str(score),
                                 True,
                                 colors.gray)
    score_rect = score_rendered.get_rect(topleft=(10, 10))

    surface.blit(score_rendered, score_rect)

    return


def create_tower(pos):
    from tower import Tower

    data = config.data

    tower_instance = Tower(pos, 'std')
    data['towers'].append(tower_instance)

    return


def parse_map(filename):
    pass
