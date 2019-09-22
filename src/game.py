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


def gameplay(surface):
    pass


def quit_game(surface):
    from pygame import quit
    from sys import exit

    quit()
    exit()
