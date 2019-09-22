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
        pickle.dump(config.data, f, protocol=-1)

    pygame.quit()
    exit()

    return


def gameplay(surface):

    data = config.data

    tower_img = pygame.image.load('../assets/tiles/tower/wR.bmp').convert()
    tower_img.set_colorkey(colors.colorkey)

    wall_tile = pygame.image.load('../assets/tiles/floor/'
                                  'dngn_rock_wall_00.bmp').convert()
    floor_tile = pygame.image.load('../assets/tiles/floor/'
                                   'dngn_floor.bmp').convert()
    path_tile = pygame.image.load('../assets/tiles/floor/'
                                  'dngn_floor_lair.bmp').convert()
    water_tile = pygame.image.load('../assets/tiles/floor/'
                                   'dngn_shallow_water.bmp').convert()
    entrance_tile = pygame.image.load('../assets/tiles/floor/'
                                      'dngn_enter_abyss.bmp').convert()
    exit_tile = pygame.image.load('../assets/tiles/floor/'
                                  'dngn_exit.bmp').convert()

    wall_tile.set_colorkey(colors.colorkey)
    floor_tile.set_colorkey(colors.colorkey)
    path_tile.set_colorkey(colors.colorkey)
    water_tile.set_colorkey(colors.colorkey)
    entrance_tile.set_colorkey(colors.colorkey)
    exit_tile.set_colorkey(colors.colorkey)

    tiles = {'wall': wall_tile,
             'floor': floor_tile,
             'upath': path_tile,
             'dpath': path_tile,
             'lpath': path_tile,
             'rpath': path_tile,
             'water': water_tile,
             'entrance': entrance_tile,
             'exit': exit_tile,
             }

    while True:
        surface.fill(colors.black)

        blit_level(surface, tiles, data['level'])

        # i need to figure out some efficiency stuff here because
        # this is ridiculous

        for tower in data['towers']:
            blit_tower(surface, tower_img, tower)

        blit_score(surface, data['score'])

        blit_wave_button(surface, data['wave'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(surface)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                create_tower(event.pos)

        pygame.display.flip()


def blit_wave_button(surface, wavenum):

    font = pygame.font.SysFont(config.fontname, config.fontsize)

    box = pygame.Surface((80, font.get_linesize()))
    box.fill(colors.bgblue)

    box_rect = box.get_rect(topleft=(10, 10))

    wave_rendered = font.render(str(wavenum),
                                True,
                                colors.black)
    wave_rect = wave_rendered.get_rect(midtop=box_rect.midtop)

    surface.blit(box, box_rect)
    surface.blit(wave_rendered, wave_rect)

    return


def blit_level(surface, tiles, level):
    game_map_file = '../assets/maps/map_{}.txt'.format(level)

    # for testing purposes
    game_map_file = '../assets/maps/test.txt'

    game_map = parse_map(game_map_file)

    tile_loc = pygame.Rect(50, 50, 32, 32)

    for row in game_map:
        for tile in row:
            surface.blit(tiles[tile], tile_loc)
            tile_loc.move_ip(32, 0)
        tile_loc.move_ip(-32 * len(row), 32)

    pass


def blit_tower(surface, tower_img, tower):

    tower_loc = tower_img.get_rect(center=(tower.x,
                                           tower.y))

    surface.blit(tower_img, tower_loc)

    return


def blit_score(surface, score):

    font = pygame.font.SysFont(config.fontname, config.fontsize)

    box = pygame.Surface((80, font.get_linesize()))
    box.fill(colors.bggreen)

    box_rect = box.get_rect(topright=(config.width - 10,
                                      10))

    score_rendered = font.render(str(score),
                                 True,
                                 colors.black)
    score_rect = score_rendered.get_rect(midtop=box_rect.midtop)

    surface.blit(box, box_rect)
    surface.blit(score_rendered, score_rect)

    return


def create_tower(pos):
    from tower import Tower

    data = config.data

    snapped_pos = (pos[0] - pos[0] % 32,
                   pos[1] - pos[1] % 32)

    # check if there is a tower already in that position
    for tower in data['towers']:
        if tower.pos == snapped_pos:
            return

    tower_instance = Tower(snapped_pos, 'std')
    data['towers'].append(tower_instance)

    return


def parse_map(filename):
    with open(filename, 'r') as f:
        raw_data = f.read().splitlines()

    game_map = []

    for num, line in enumerate(raw_data):
        row = []
        for charnum, character in enumerate(line):
            if character == '#':
                tile = 'wall'
            elif character == 'w':
                tile = 'water'
            elif character == '.':
                tile = 'floor'
            elif character == 'v':
                tile = 'dpath'
            elif character == '^':
                tile = 'upath'
            elif character == '>':
                tile = 'rpath'
            elif character == '<':
                tile = 'lpath'

            if num == 0:
                if character == 'v':
                    tile = 'entrance'
                elif character == '^':
                    tile = 'exit'
            elif num == len(raw_data) - 1:
                if character == '^':
                    tile = 'entrance'
                elif character == 'v':
                    tile = 'exit'
            elif charnum == 0:
                if character == '>':
                    tile = 'entrance'
                elif character == '<':
                    tile = 'exit'
            elif charnum == len(line) - 1:
                if character == '<':
                    tile = 'entrance'
                if character == '>':
                    tile = 'exit'

            row.append(tile)
        game_map.append(row)

    return game_map
