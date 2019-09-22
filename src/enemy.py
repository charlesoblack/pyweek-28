#! /usr/bin/env python3


class Enemy(object):

    def __init__(self, pos, enemy_type):
        self.x = pos[0]
        self.y = pos[1]
        self.type = enemy_type
        self.dead = False
        self.last_move = 0

    def move_forward(self, game_map):
        if self.dead:
            return
        if self.last_move < 10:
            self.last_move += 1
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

        self.last_move = 0
