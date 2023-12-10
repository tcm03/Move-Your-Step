import os
import sys
import time
from random import choice
import pygame

from level1.level1_map import level1_play

def option_choose1():


    pygame.init()

    
    screen = pygame.display.set_mode((800, 600))

    
    buttons = [pygame.Rect(100 + i*120, 300, 100, 50) for i in range(5)]
    button_texts = ['A*', 'BFS', 'DFS','UCS', 'Exit']
    button_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),(0, 255, 255)]


    
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
                        if button_texts[idx] == 'A*':
                            check = 1
                        if button_texts[idx] == 'BFS':
                            check = 2
                        if button_texts[idx] == 'DFS':
                            check = 3
                        if button_texts[idx] == 'UCS':
                            check = 4
                        if button_texts[idx] == 'Exit':
                            return True
                        level1_play(check)

        screen.fill((255, 255, 255))

        # Vẽ tiêu đề
        screen.blit(title, (200, 50))

        for idx, button in enumerate(buttons):
            pygame.draw.rect(screen, button_colors[idx], button)
            label = button_labels[idx]
            label_pos = label.get_rect(center=button.center)
            screen.blit(label, label_pos)

        pygame.display.flip()
