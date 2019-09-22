#! /usr/bin/env python3

width = 1000
height = 800
fontname = 'Arial'
fontsize = 32
data = {'level': 1,
        'score': 0,
        'towers': [],
        'money': 50,
        'wave': 1,
        'core': 30,
        }
wave_active = False
active_enemies = []
game_map = None
tile_size = 32
map_size = 20
offset_l = width // 2 - map_size * tile_size // 2
offset_r = width // 2 + map_size * tile_size // 2
offset_u = height // 2 - map_size * tile_size // 2
offset_d = height // 2 + map_size * tile_size // 2
game_speed = 10
