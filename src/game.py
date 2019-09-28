#! /usr/bin/env python3

import pygame
import config
import colors
import os
import random


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

    os.makedirs('../data', exist_ok=True)

    with open('../data/saved_data.pckl', 'wb') as f:
        pickle.dump(config.data, f, protocol=-1)

    pygame.quit()
    exit()

    return


def gameplay(surface):
    from numpy import subtract
    from copy import deepcopy

    data = config.data

    tower_img_white = pygame.image.load('../assets/tiles/tower/wR.bmp').convert()
    tower_img_white.set_colorkey(colors.colorkey)

    tower_img_red = tower_img_white.copy()
    tower_img_red.fill(colors.purered, special_flags=pygame.BLEND_MIN)

    tower_img_blue = tower_img_white.copy()
    tower_img_blue.fill(colors.pureblue, special_flags=pygame.BLEND_MIN)

    tower_img_green = tower_img_white.copy()
    tower_img_green.fill(colors.puregreen, special_flags=pygame.BLEND_MIN)

    tower_imgs = {'white': tower_img_white,
                  'red': tower_img_red,
                  'blue': tower_img_blue,
                  'green': tower_img_green}

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

    enemy_imgs = {}
    enemy_types = []
    for file in os.listdir('../assets/tiles/enemy/'):
        img = pygame.image.load('../assets/tiles/enemy/{}'.format(file))
        img = img.convert()
        img.set_colorkey(colors.colorkey)
        enemy_imgs[file[:-4]] = img
        enemy_types.append(file[:-4])

    new_wave(enemy_types)

    parse_map(data['level'])
    clock = pygame.time.Clock()
    width_8 = config.width / 8

    while True:
        surface.fill(colors.black)

        blit_level(surface, tiles)

        # i need to figure out some efficiency stuff here because
        # this is ridiculous

        for tower in data['towers']:
            blit_tower(surface, tower_imgs, tower)

        # wave number
        blit_info(surface,
                  (width_8, 10),
                  colors.bgblue,
                  'Wave {}-{}'.format(data['level'], data['wave']))

        # money
        blit_info(surface,
                  (3 * width_8, 10),
                  colors.bgyellow,
                  'Money: {}'.format(data['money']))

        # core
        blit_info(surface,
                  (5 * width_8, 10),
                  colors.bgred,
                  'Core: {}'.format(data['core']))

        # score
        blit_info(surface,
                  (7 * width_8, 10),
                  colors.bggreen,
                  'Score: {}'.format(data['score']))

        blit_next_wave(surface)

        if config.wave_active:
            blit_enemies(surface,
                         enemy_imgs,
                         config.enemies)

            blit_shots(surface,
                       data['towers'])

        if config.wave_active and all(enemy.dead
                                      for enemy in config.active_enemies):
            config.wave_active = False
            config.active_enemies = []
            data['wave'] += 1
            new_wave(enemy_types)

        if data['wave'] > 10:
            data['wave'] = 1
            data['level'] += 1
            parse_map(data['level'])

        if config.wave_active:
            for enemy in config.active_enemies:
                enemy.move_forward()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(surface)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                issue_command(event.pos)

        clock.tick(60)
        pygame.display.flip()


def new_wave(enemy_types):
    config.this_wave = config.next_wave or [random.choice(enemy_types)]
    enemy_count = random.randrange(10, 20) * config.data['wave']
    config.enemies = [random.choice(config.this_wave)
                      for _ in range(enemy_count)]
    if config.tactic == 'many-of-one':
        config.next_wave = [random.choice(enemy_types)]
    elif config.tactic == 'large-hp':
        config.next_wave = random.choices(enemy_types, k=2)
    elif config.tactic == 'few-of-many':
        config.next_wave = random.choices(enemy_types, k=5)
    config.tactic = random.choice(['many-of-one',
                                   'large-hp',
                                   'few-of-many'])

    return


def blit_shots(surface, towers):
    for tower in towers:
        tower.find_enemy(config.active_enemies)
        tower.shoot(surface)
    return


def blit_next_wave(surface):
    font = pygame.font.SysFont(config.fontname, config.fontsize)

    box = pygame.Surface((320, font.get_linesize()))
    box.fill(colors.bggray)

    rect = box.get_rect(midtop=(config.width // 2,
                                config.height - font.get_linesize() - 10))

    text = font.render('Start next wave!',
                       True,
                       colors.black)
    text_rect = text.get_rect(midtop=rect.midtop)

    surface.blit(box, rect)
    surface.blit(text, text_rect)

    return


def blit_info(surface, pos, color, text):

    font = pygame.font.SysFont(config.fontname, config.fontsize)

    box = pygame.Surface((160, font.get_linesize()))
    box.fill(color)

    box_rect = box.get_rect(midtop=(round(pos[0]),
                                    round(pos[1])))

    text_rendered = font.render(text,
                                True,
                                colors.black)
    text_rect = text_rendered.get_rect(midtop=box_rect.midtop)

    surface.blit(box, box_rect)
    surface.blit(text_rendered, text_rect)

    return


def blit_level(surface, tiles):

    tile_loc = pygame.Rect(config.offset_l + config.tile_size // 2,
                           config.offset_u,
                           config.tile_size,
                           config.tile_size)

    for row in config.game_map.raw:
        for tile in row:
            surface.blit(tiles[tile], tile_loc)
            tile_loc.move_ip(config.tile_size,
                             0)
        tile_loc.move_ip(-config.tile_size * len(row),
                         config.tile_size)

    return


def blit_tower(surface, tower_imgs, tower):

    tower_loc = tower_imgs[tower.type].get_rect(topleft=(tower.x_converted,
                                                         tower.y_converted))

    surface.blit(tower_imgs[tower.type], tower_loc)

    return


def blit_enemies(surface, enemy_imgs, enemies):
    from enemy import Enemy

    entrance_loc = (config.game_map.entrance[0],
                    config.game_map.entrance[1])

    if enemies:
        if (not config.active_enemies or
                config.active_enemies[-1].last_action == 0):
            config.active_enemies.append(Enemy(entrance_loc, enemies.pop(0)))
    for enemy in config.active_enemies:
        if not enemy.dead:
            surface.blit(enemy_imgs[enemy.type],
                         pygame.Rect(enemy.x_converted,
                                     enemy.y_converted,
                                     enemy_imgs[enemy.type].get_width(),
                                     enemy_imgs[enemy.type].get_height()))
    return


def issue_command(mouse_pos):
    width = config.width
    height = config.height

    font = pygame.font.SysFont(config.fontname, config.fontsize)
    linesize = font.get_linesize()

    offset_l = config.offset_l + config.tile_size
    offset_r = config.offset_r - config.tile_size
    offset_u = config.offset_u + config.tile_size
    offset_d = config.offset_d - config.tile_size

    if (offset_l <= mouse_pos[0] <= offset_r and
            offset_u <= mouse_pos[1] <= offset_d):
        create_tower(mouse_pos)
    if ((width // 2 - 160 <= mouse_pos[0] <= width // 2 + 160) and
            height - linesize - 10 <= mouse_pos[1] <= height - 10 and
            not config.wave_active):
        config.wave_active = True

    return


def create_tower(pos):
    from tower import Tower

    data = config.data

    snapped_pos = ((pos[0]
                    - config.offset_l
                    - config.tile_size // 2) // config.tile_size,
                   (pos[1] - config.offset_u) // config.tile_size)

    # check if there is a tower already in that position
    for tower in data['towers']:
        if tower.pos == snapped_pos:
            tower.upgrade()
            return

    if (data['money'] >= 10 and
            config.game_map.raw[snapped_pos[1]][snapped_pos[0]] == 'floor'):
        tower_instance = Tower(snapped_pos, 'white')
        data['towers'].append(tower_instance)
        data['money'] = data['money'] - 10

    return


def parse_map(level):
    import maps

    game_map_file = '../assets/maps/map_{}.txt'.format(level)

    # for testing purposes
    game_map_file = '../assets/maps/test.txt'

    with open(game_map_file, 'r') as f:
        raw_data = f.read().splitlines()

    game_map = maps.Map()

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

            if tile in ('entrance', 'exit'):
                setattr(game_map, tile, (charnum, num))

            row.append(tile)
        game_map.raw.append(row)

    config.game_map = game_map

    return
