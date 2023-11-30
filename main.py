import os
import sys
import time
from random import choice
import pygame
from level1.start_level1 import option_choose1

from level2.level2_map import level2_play
from level2.start_level2 import option_choose2
from level3.level3_map import level3_play
from level3.start_level3 import option_choose3


# Khởi tạo Pygame
pygame.init()

# Thiết lập kích thước cửa sổ
screen = pygame.display.set_mode((800, 600))

# Tạo 5 nút bấm
buttons = [pygame.Rect(100 + i*120, 300, 100, 50) for i in range(5)]
button_texts = ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Exit']
button_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)]

# Tạo font chữ
font_button = pygame.font.Font(None, 24)
font_title = pygame.font.Font(None, 72)

# Tạo chữ cho các nút và tiêu đề
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
                if button.collidepoint(mouse_pos):
                    print(f'{button_texts[idx]} đã được nhấn!')
                    if button_texts[idx] == 'Level 1':
                        if option_choose1():
                            continue
                    if button_texts[idx] == 'Level 2':
                        if option_choose2():
                            continue
                    if button_texts[idx] == 'Level 3':
                        if option_choose3():
                            continue
                    if button_texts[idx] == 'Exit':
                        pygame.quit()
                        sys.exit()

    screen.fill((255, 255, 255))

    # Vẽ tiêu đề
    screen.blit(title, (200, 50))

    for idx, button in enumerate(buttons):
        pygame.draw.rect(screen, button_colors[idx], button)
        label = button_labels[idx]
        label_pos = label.get_rect(center=button.center)
        screen.blit(label, label_pos)

    pygame.display.flip()
