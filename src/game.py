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


def endless(surface):

    config.mode = 'endless'

    gameplay(surface)
    return


def new_game(surface):

    config.mode = 'campaign'

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

    data = config.data
    font = pygame.font.SysFont(config.fontname, config.fontsize)

    tower_types = {'color': {'white': colors.white,
                             'red': colors.purered,
                             'blue': colors.pureblue,
                             'green': colors.puregreen,
                             }}

    # ================================== GUI ==================================

    tower_type_text = font.render('Tower type',
                                  True,
                                  colors.white)

    tower_sqr_white = pygame.Surface((config.tile_size,
                                      config.tile_size))
    tower_sqr_white.fill(tower_types['color']['white'])

    tower_sqr_red = pygame.Surface((config.tile_size,
                                    config.tile_size))
    tower_sqr_red.fill(tower_types['color']['red'])

    tower_sqr_green = pygame.Surface((config.tile_size,
                                      config.tile_size))
    tower_sqr_green.fill(tower_types['color']['green'])

    tower_sqr_blue = pygame.Surface((config.tile_size,
                                     config.tile_size))
    tower_sqr_blue.fill(tower_types['color']['blue'])

    tower_sqr = tower_sqr_white.get_rect(midtop=((config.width
                                                  + config.offset_r)
                                                 // 2,
                                                 config.height // 2
                                                 + font.get_linesize()))
    type_text_rect = tower_type_text.get_rect(midbottom=tower_sqr.midtop)

    tower_types['gui_square'] = {'white': tower_sqr_white,
                                 'red': tower_sqr_red,
                                 'blue': tower_sqr_blue,
                                 'green': tower_sqr_green,
                                 }

    # ================================ Towers =================================

    tower_white_1 = pygame.image.load('./assets/tiles/tower/'
                                      'wR_magenta.bmp').convert()

    tower_white_2 = tower_white_1.copy()
    tower_white_2.fill(colors.puregray_6,
                       special_flags=pygame.BLEND_MIN)

    tower_white_3 = tower_white_1.copy()
    tower_white_3.fill(colors.puregray_2,
                       special_flags=pygame.BLEND_MIN)

    tower_red_1 = tower_white_1.copy()
    tower_red_1.fill(colors.purered, special_flags=pygame.BLEND_MIN)

    # the exception because our sprite has a magenta background
    tower_red_2 = tower_white_1.copy()
    tower_red_2.fill(colors.purered_5,
                     special_flags=pygame.BLEND_SUB)

    tower_blue_1 = tower_white_1.copy()
    tower_blue_1.fill(colors.pureblue, special_flags=pygame.BLEND_MIN)

    tower_blue_2 = tower_white_1.copy()
    tower_blue_2.fill(colors.pureblue_8,
                      special_flags=pygame.BLEND_MIN)

    tower_blue_3 = tower_white_1.copy()
    tower_blue_3.fill(colors.pureblue_6,
                      special_flags=pygame.BLEND_MIN)

    tower_blue_4 = tower_white_1.copy()
    tower_blue_4.fill(colors.pureblue_4,
                      special_flags=pygame.BLEND_MIN)

    tower_blue_5 = tower_white_1.copy()
    tower_blue_5.fill(colors.pureblue_2,
                      special_flags=pygame.BLEND_MIN)

    tower_green_1 = tower_white_1.copy()
    tower_green_1.fill(colors.puregreen, special_flags=pygame.BLEND_MIN)

    tower_green_2 = tower_white_1.copy()
    tower_green_2.fill(colors.puregreen_5,
                       special_flags=pygame.BLEND_MIN)

    tower_types['sprites'] = {1: {'white': tower_white_1,
                                  'red': tower_red_1,
                                  'blue': tower_blue_1,
                                  'green': tower_green_1,
                                  },
                              2: {'white': tower_white_2,
                                  'red': tower_red_2,
                                  'blue': tower_blue_2,
                                  'green': tower_green_2,
                                  },
                              3: {'white': tower_white_3,
                                  'blue': tower_blue_3,
                                  },
                              4: {'blue': tower_blue_4,
                                  },
                              5: {'blue': tower_blue_5,
                                  },
                              }

    for lvl in tower_types['sprites'].values():
        for img in lvl.values():
            img.set_colorkey(img.get_at((0, 0)))

    # ================================== Map ==================================

    wall_tile = pygame.image.load('./assets/tiles/floor/'
                                  'dngn_rock_wall_00.bmp').convert()
    floor_tile = pygame.image.load('./assets/tiles/floor/'
                                   'dngn_floor.bmp').convert()
    path_tile = pygame.image.load('./assets/tiles/floor/'
                                  'dngn_floor_lair.bmp').convert()
    water_tile = pygame.image.load('./assets/tiles/floor/'
                                   'dngn_shallow_water.bmp').convert()
    entrance_tile = pygame.image.load('./assets/tiles/floor/'
                                      'dngn_enter_abyss.bmp').convert()
    exit_tile = pygame.image.load('./assets/tiles/floor/'
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

    # ================================ Enemies ================================

    enemy_imgs = {}
    enemy_types = []
    for file in os.listdir('./assets/tiles/enemy/'):
        img = pygame.image.load('./assets/tiles/enemy/{}'.format(file))
        img = img.convert()
        img.set_colorkey(colors.colorkey)
        enemy_imgs[file[:-4]] = img
        enemy_types.append(file[:-4])

    # ============================== Other prep ===============================

    new_wave(enemy_types)

    new_map()
    clock = pygame.time.Clock()
    width_8 = config.width / 8

    while True:
        if ((data['level'] > 10 and config.mode == 'campaign') or
                (data['core'] <= 0)):
            break

        surface.fill(colors.black)

        surface.blit(tower_types['gui_square'][config.tower_type],
                     tower_sqr)
        surface.blit(tower_type_text, type_text_rect)

        blit_level(surface, tiles)

        # i need to figure out some efficiency stuff here because
        # this is ridiculous

        for tower in data['towers']:
            blit_tower(surface, tower_types['sprites'], tower)

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
            data['towers'] = []
            data['core'] = 30
            new_map()

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

    credits(surface)
    return


def credits(surface):
    font = pygame.font.SysFont(config.fontname, config.fontsize)
    linesize = font.get_linesize()

    score = font.render('Your final score was {}'.format(config.data['score']),
                        True,
                        colors.white)
    score_rect = score.get_rect(midtop=(config.width // 2,
                                        config.height // 2 - linesize))

    author = font.render('Author: sid',
                         True,
                         colors.white)
    author_rect = author.get_rect(midtop=score_rect.midbottom)

    artwork = font.render('Artwork by the RLTiles folks and @therealqtpi',
                          True,
                          colors.white)
    artwork_rect = artwork.get_rect(midtop=author_rect.midbottom)

    any_key = font.render('Press any key to continue...',
                          True,
                          colors.white)
    any_rect = any_key.get_rect(midtop=artwork_rect.midbottom)

    surface.fill(colors.black)

    surface.blit(score, score_rect)
    surface.blit(author, author_rect)
    surface.blit(artwork, artwork_rect)

    pygame.display.flip()

    # waiting 5s
    pygame.time.wait(5000)

    surface.blit(any_key, any_rect)

    pygame.display.flip()

    pygame.event.clear()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(surface)
            elif event.type == pygame.KEYDOWN:
                return
    return


def new_wave(enemy_types):
    config.this_wave = config.next_wave or [random.choice(enemy_types)]
    enemy_count = random.randrange(10, 20) * config.data['wave']
    if config.tactic == 'large-hp':
        enemy_count = enemy_count // 3 + 1
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


def new_map():
    if config.mode == 'endless':
        create_map()
    else:
        parse_map(config.data['level'])
    return


def create_map():
    import maps

    game_map = maps.Map()
    map_size = config.map_size

    # generate a map on the fly here

    # generate entrance/exit locations
    entrance_loc = [random.randrange(1, map_size - 2),
                    random.choice([0, map_size - 1]),
                    ]
    random.shuffle(entrance_loc)  # to make it nice and even

    # generate empty map
    for row_num in range(map_size):
        if row_num in (0, map_size - 1):
            row = ['wall' for _ in range(map_size)]
        else:
            row = (['wall']
                   + ['floor' for _ in range(map_size - 2)]
                   + ['wall'])
        game_map.raw.append(row)

    # place entrance/exit
    setattr(game_map, 'entrance', tuple(entrance_loc))
    game_map.raw[entrance_loc[1]][entrance_loc[0]] = 'entrance'

    # find a path
    vertex = entrance_loc
    last_vertex = None

    for iter_count in range(20):
        corridor_len = random.randint(2, 6)
        corridor_dir = random.choice(['dpath',
                                      'upath',
                                      'rpath',
                                      'lpath'])

        if last_vertex is not None:
            game_map.raw[vertex[1]][vertex[0]] = corridor_dir

        if corridor_dir == 'upath':
            for v in range(corridor_len):
                loc = game_map.raw[vertex[1] - 1][vertex[0]]
                if loc in ('upath', 'dpath', 'rpath', 'lpath', 'wall'):
                    break
                game_map.raw[vertex[1] - 1][vertex[0]] = 'upath'
                last_vertex = list(vertex)
                vertex[1] -= 1

        elif corridor_dir == 'dpath':
            for v in range(corridor_len):
                try:
                    loc = game_map.raw[vertex[1] + 1][vertex[0]]
                    if loc in ('upath', 'dpath', 'rpath', 'lpath', 'wall'):
                        break
                    game_map.raw[vertex[1] + 1][vertex[0]] = 'dpath'
                    last_vertex = list(vertex)
                    vertex[1] += 1
                except IndexError:
                    pass

        elif corridor_dir == 'rpath':
            for v in range(corridor_len):
                try:
                    loc = game_map.raw[vertex[1]][vertex[0] + 1]
                    if loc in ('upath', 'dpath', 'rpath', 'lpath', 'wall'):
                        break
                    game_map.raw[vertex[1]][vertex[0] + 1] = 'rpath'
                    last_vertex = list(vertex)
                    vertex[0] += 1
                except IndexError:
                    pass

        elif corridor_dir == 'lpath':
            for v in range(corridor_len):
                loc = game_map.raw[vertex[1]][vertex[0] - 1]
                if loc in ('upath', 'dpath', 'rpath', 'lpath', 'wall'):
                    break
                game_map.raw[vertex[1]][vertex[0] - 1] = 'lpath'
                last_vertex = list(vertex)
                vertex[0] -= 1

    setattr(game_map, 'exit', tuple(vertex))
    game_map.raw[vertex[1]][vertex[0]] = 'exit'

    # place water tiles for looking nice using drunkard walk

    amt = int(0.1 * map_size ** 2)
    count = 0

    random_loc = [random.randint(1, map_size - 2),
                  random.randint(1, map_size - 2)]
    current_loc = random_loc

    while count < amt:
        old_loc = list(current_loc)

        # if we are not in a path
        if game_map.raw[current_loc[1]][current_loc[0]] == 'floor':
            game_map.raw[current_loc[1]][current_loc[0]] = 'water'
            count += 1
        else:
            current_loc = old_loc

        new_area = random.randint(1, 100) <= 10

        if not new_area:
            direction = random.choice(['down', 'up', 'left', 'right'])
            if direction == 'down':
                current_loc[1] += 1
            elif direction == 'up':
                current_loc[1] -= 1
            elif direction == 'right':
                current_loc[0] += 1
            elif direction == 'left':
                current_loc[0] -= 1

            # prevent walking off the map
            current_loc[0] = max(current_loc[0], 1)
            current_loc[1] = max(current_loc[1], 1)
            current_loc[0] = min(current_loc[0], map_size - 2)
            current_loc[1] = min(current_loc[1], map_size - 2)

        else:
            current_loc = [random.randint(1, map_size - 2),
                           random.randint(1, map_size - 2)]

    config.game_map = game_map

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
    tower_img = tower_imgs[tower.level][tower.type]
    tower_loc = tower_img.get_rect(topleft=(tower.x_converted,
                                            tower.y_converted))

    surface.blit(tower_img, tower_loc)

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

    # if we're clicking somewhere in the field of play
    if (offset_l <= mouse_pos[0] <= offset_r and
            offset_u <= mouse_pos[1] <= offset_d):

        # create a new tower
        create_tower(mouse_pos)

    # if we're clicking on the "next wave" button
    if ((width // 2 - 160 <= mouse_pos[0] <= width // 2 + 160) and
            height - linesize - 10 <= mouse_pos[1] <= height - 10 and
            not config.wave_active):

        # start the next wave
        config.wave_active = True

    # if we're clicking on the tower type icon
    if (((width + config.offset_r - config.tile_size) // 2 <=
         mouse_pos[0] <=
         (width + config.offset_r + config.tile_size) // 2) and
        (height // 2 + linesize <=
         mouse_pos[1] <=
         height // 2 + linesize + config.tile_size)):

        # change the tower type
        new_index = ((config.tower_types.index(config.tower_type)
                      + 1)
                     % len(config.tower_types)
                     ) or 0  # guarantee that we have something, at least
        config.tower_type = config.tower_types[new_index]

    return


def create_tower(pos):
    from tower import Tower

    data = config.data
    tower_type = config.tower_type

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
        tower_instance = Tower(snapped_pos, tower_type)
        data['towers'].append(tower_instance)
        data['money'] = data['money'] - 10

    return


def parse_map(level):
    import maps

    game_map_file = './assets/maps/map_{}.txt'.format(level)

    # for testing purposes
    # game_map_file = './assets/maps/test.txt'

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
