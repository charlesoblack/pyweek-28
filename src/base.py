#! /usr/bin/env python3

import config


class BaseEntity(object):

    def __init__(self, pos, entity_type):
        self.x, self.y = pos
        self.type = entity_type
        self.last_action = 0

    @property
    def pos(self):
        return (self.x, self.y)

    @property
    def x_converted(self):
        return (self.x + 0.5) * config.tile_size + config.offset_l

    @property
    def y_converted(self):
        return self.y * config.tile_size + config.offset_u
