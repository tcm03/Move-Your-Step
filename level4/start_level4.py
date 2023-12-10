

import sys
import pygame

from level4.level4_map import level4_play


def option_choose4():

    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    buttons = [pygame.Rect(280 + i*120, 300, 100, 50) for i in range(2)]
    button_texts = ['Start','Exit']
    button_colors = [(255, 0, 0), (0, 255, 0)]
    
    font_button = pygame.font.Font(None, 24)
    font_title = pygame.font.Font(None, 72)

    title = font_title.render('MOVE YOUR STEP', True, (0, 0, 0))
    button_labels = [font_button.render(text, True, (0, 0, 0)) for text in button_texts]



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for idx, button in enumerate(buttons):
                    check = 1
                    if button.collidepoint(mouse_pos):
                        if button_texts[idx] == 'Start':
                            check = 1
                        if button_texts[idx] == 'Exit':
                            return True
                        level4_play(check)

        screen.fill((255, 255, 255))

        screen.blit(title, (200, 50))

        for idx, button in enumerate(buttons):
            pygame.draw.rect(screen, button_colors[idx], button)
            label = button_labels[idx]
            label_pos = label.get_rect(center=button.center)
            screen.blit(label, label_pos)

        pygame.display.flip()
