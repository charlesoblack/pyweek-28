#! /usr/bin/env python3

import config
import base


class Enemy(base.BaseEntity):

    def __init__(self, *params):
        super().__init__(*params)
        self.health = 5

    def take_dmg(self, amt):
        self.health = max(0, self.health - amt)
        return

    @property
    def dead(self):
        return self.health <= 0

    def move_forward(self):
        if self.dead:
            return
        if self.last_action < 30:
            self.last_action += 1
            return

        tile = config.game_map.raw[self.y][self.x]

        if tile == 'rpath':
            self.x += 1
        elif tile == 'lpath':
            self.x -= 1
        elif tile == 'dpath':
            self.y += 1
        elif tile == 'upath':
            self.y -= 1
        elif tile == 'entrance':
            if self.x == len(config.game_map.raw[self.y]):
                self.x -= 1
            elif self.x == 0:
                self.x += 1
            elif self.y == 0:
                self.y += 1
            else:
                self.y -= 1

        if config.game_map.raw[self.y][self.x] == 'exit':
            self.health = 0
            config.data['core'] -= 1

        self.last_action = 0

        return
