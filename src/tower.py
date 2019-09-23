#! /usr/bin/env python3

import pygame
import colors
import base
import config
import random


class Tower(base.BaseEntity):

    def __init__(self, *params):
        super().__init__(*params)
        self.damage = 1
        self.level = 1
        self.upgrade_cost = 20
        self.current_enemy = None
        self.max_level = 3
        self.range = 2

    def distance(self, enemy):
        return abs(self.x - enemy.x) ** 2 + abs(self.y - enemy.y) ** 2

    def find_enemy(self, enemies):
        if (self.current_enemy is not None and
                self.distance(self.current_enemy) < self.range):
            return

        self.current_enemy = None

        distance = 0
        for enemy in enemies:
            if not enemy.dead:
                new_distance = self.distance(enemy)
                if distance < new_distance <= self.range:
                    self.current_enemy = enemy

    def shoot(self, surface):
        if self.current_enemy is not None:
            if self.last_action < config.game_speed:
                self.last_action += 1
                return

            tilesize = config.tile_size
            pygame.draw.line(surface,
                             colors.shots,
                             (self.x_converted + tilesize // 2,
                              self.y_converted + tilesize // 2),
                             (self.current_enemy.x_converted + tilesize // 2,
                              self.current_enemy.y_converted + tilesize // 2),
                             2)

            self.current_enemy.take_dmg(self.damage)
            config.data['score'] += 10
            if self.current_enemy.dead:
                self.current_enemy = None
                config.data['money'] += 1
                config.data['score'] += 90
            self.last_action = 0

        return

    def upgrade(self):
        if (config.data['money'] >= self.upgrade_cost and
                self.level < self.max_level):
            self.level = max(self.level + 1, self.max_level)
            self.damage += random.choices(range(1, 6),
                                          weights=[0.4,  # 1
                                                   0.2,  # 2
                                                   0.2,  # 3
                                                   0.1,  # 4
                                                   0.1,  # 5
                                                   ])[0]
            self.range += 1
            config.data['money'] -= self.upgrade_cost
            self.upgrade_cost += 20 * self.level

        return
