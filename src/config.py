#! /usr/bin/env python3

width = 740
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
offset_l = 50
offset_r = width - offset_l
offset_u = 50
offset_d = offset_u + 20 * tile_size
game_speed = 10
