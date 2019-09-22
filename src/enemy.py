#! /usr/bin/env python3


class Enemy(object):

    def __init__(self, pos, enemy_type):
        self.x = pos[0]
        self.y = pos[1]
        self.type = enemy_type
        self.dead = False
