#! /usr/bin/env python3


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
        return self.x * 32 + 50

    @property
    def y_converted(self):
        return self.y * 32 + 50
