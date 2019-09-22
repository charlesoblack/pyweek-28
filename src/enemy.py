#! /usr/bin/env python3

import config
import base


class Enemy(base.BaseEntity):

    def __init__(self, *params):
        super().__init__(*params)
        self.dead = False

    def move_forward(self, game_map):
        if self.dead:
            return
        if self.last_action < 30:
            self.last_action += 1
            return

        tile = game_map.raw[self.y][self.x]

        if tile == 'rpath':
            self.x += 1
        elif tile == 'lpath':
            self.x -= 1
        elif tile == 'dpath':
            self.y += 1
        elif tile == 'upath':
            self.y -= 1
        elif tile == 'entrance':
            if self.x == len(game_map.raw[self.y]):
                self.x -= 1
            elif self.x == 0:
                self.x += 1
            elif self.y == 0:
                self.y += 1
            else:
                self.y -= 1

        if game_map.raw[self.y][self.x] == 'exit':
            self.dead = True
            config.data['core'] -= 1

        self.last_action = 0

        return
