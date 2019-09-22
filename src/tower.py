#! /usr/bin/env python3

import pygame
import colors
import base


class Tower(base.BaseEntity):

    def __init__(self, *params):
        super().__init__(*params)
        self.damage = 1
        self.level = 1
        self.current_enemy = None
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
            if self.last_action < 10:
                self.last_action += 1
                return

            pygame.draw.line(surface,
                             colors.shots,
                             (self.x_converted + 16,
                              self.y_converted + 16),
                             (self.current_enemy.x_converted + 16,
                              self.current_enemy.y_converted + 16),
                             2)

            self.current_enemy.take_dmg(self.damage)
            if self.current_enemy.dead:
                self.current_enemy = None
            self.last_action = 0

        return
