#! /usr/bin/env python3

import pygame
import config


def continue_game(surface):
    import pickle

    # make sure that we actually have the data if we select this

    with open('../data/saved_data.pckl', 'rb') as f:
        data = pickle.load(f)

    config.data = data

    gameplay(surface)

    return


def quit_game(surface):
    from sys import exit
    import pickle
    import os

    os.makedirs('../data', exist_ok=True)

    with open('../data/saved_data.pckl', 'wb') as f:
        pickle.dump(f, config.data, protocol=-1)

    pygame.quit()
    exit()

    return


def gameplay(surface):
    import colors

    data = config.data

    while True:
        surface.fill(colors.black)

        blit_level(surface, data['level'])

        for tower in data['towers']:
            blit_tower(surface, tower)

        blit_score(surface, data['score'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(surface)
            elif event.type == pygame.KEYDOWN:
                pass

        pygame.display.flip()


def blit_level(surface, level):
    pass


def blit_tower(surface, tower):
    pass


def blit_score(surface, score):
    import colors

    font = pygame.font.SysFont(config.fontname, config.fontsize)

    score_rendered = font.render(str(score),
                                 True,
                                 colors.gray)
    score_rect = score_rendered.get_rect(topleft=(10, 10))

    surface.blit(score_rendered, score_rect)

    return
