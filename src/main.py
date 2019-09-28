#! /usr/bin/env python3


def main_menu(surface):
    import config
    import colors
    import pygame
    import game

    font = pygame.font.SysFont(config.fontname, config.fontsize)
    linesize = font.get_linesize()

    options = ['new',
               'continue',
               'endless',
               'quit',
               ]
    k = len(options)

    options_rendered = [font.render(option,
                                    True,
                                    colors.white)
                        for option in options]

    option_functions = [game.gameplay,
                        game.continue_game,
                        game.endless,
                        game.quit_game,
                        ]

    selection_arrow = font.render('>',
                                  True,
                                  colors.white)

    selected = 0

    while True:
        surface.fill(colors.black)

        for i, option in enumerate(options_rendered):
            loc = (config.width // 2,
                   config.height // 2 + (i - 1) * linesize)
            option_loc = option.get_rect(midtop=loc)
            surface.blit(option, option_loc)

        selection_loc = (config.width * 0.4,
                         config.height // 2 + (selected - 1) * linesize)

        surface.blit(selection_arrow,
                     selection_arrow.get_rect(midtop=selection_loc))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit_game(surface)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1 + k) % k
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1 + k) % k
                elif event.key == pygame.K_RETURN:
                    # call the appropriate function
                    option_functions[selected](surface)

        pygame.display.flip()

    return


if __name__ == '__main__':
    import pygame
    import config

    pygame.display.init()
    pygame.font.init()

    play_surface = pygame.display.set_mode((config.width, config.height))
    pygame.display.set_caption('pyweek 28')

    main_menu(play_surface)
