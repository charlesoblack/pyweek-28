#! /usr/bin/env python3


class Tower(object):

    def __init__(self, pos, tower_type):
        self.x = pos[0]
        self.y = pos[1]
        self.damage = 1
        self.level = 1
        self.type = tower_type
