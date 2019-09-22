#! /usr/bin/env python3


def continue_game(surface):
    import pickle
    import config

    # make sure that we actually have the data if we select this

    with open('../data/saved_data.pckl', 'rb') as f:
        data = pickle.load(f)

    config.data = data

    gameplay(surface)

    return


def quit_game(surface):
    from pygame import quit
    from sys import exit
    import config
    import pickle
    import os

    os.makedirs('../data', exist_ok=True)

    with open('../data/saved_data.pckl', 'wb') as f:
        pickle.dump(f, config.data, protocol=-1)

    quit()
    exit()

    return


def gameplay(surface):
    # import config
    import colors
    import pygame

    # data = config.data

    while True:
        surface.fill(colors.black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(surface)
            elif event.type == pygame.KEYDOWN:
                pass

        pygame.display.flip()
