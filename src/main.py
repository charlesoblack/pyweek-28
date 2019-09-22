#! /usr/bin/env python3


def main_menu(surface):
    pass


if __name__ == '__main__':
    import pygame
    import config

    pygame.display.init()
    pygame.font.init()

    play_surface = pygame.display.set_mode((config.width, config.height))
    pygame.display.set_caption('pyweek 28')

    main_menu(play_surface)
