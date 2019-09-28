#! /usr/bin/env python3

import config
import base
import random


class Enemy(base.BaseEntity):

    def __init__(self, *params):
        super().__init__(*params)
        self.health = random.randint(config.data['wave']
                                     * config.data['level'],
                                     config.data['wave']
                                     * (config.data['level']
                                     + 5))
        if config.tactic == 'large-hp':
            self.health *= 3
        return

    def take_dmg(self, amt):
        self.health = max(0, self.health - amt)
        return

    @property
    def dead(self):
        return self.health <= 0

    def move_forward(self):
        if self.dead:
            return
        if self.last_action < 3 * config.game_speed:
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
            if self.x == len(config.game_map.raw[self.y]) - 1:
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
