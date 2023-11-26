import sys
import time
from random import choice
import pygame
from custom_parser import read_input
from solver import breadth_first_search

map_game = read_input("input.txt")

n_floor = len(map_game)


def map_read(current):
    every_map = []
    for i in range(n_floor):
        map_i = current[i]
        current_map = [Cell(col, row, map_i[row][col]) for row in range(len(current[i])) for col in
                       range(len(current[i][0]))]
        every_map.append(current_map)
    return every_map


TILE = 25

class Cell:
    def __init__(self, x, y, text='0', color_intense=1):
        self.x, self.y = x, y
        self.text = text
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.color_intense = color_intense

    def draw_current_cell(self, screen):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(screen, pygame.Color('saddlebrown'), (x + 2, y + 2, TILE - 2, TILE - 2))

    def draw(self, distance, screen, font_use):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(screen, (
                int(255 * self.color_intense), int(255 * self.color_intense), int(153 * self.color_intense)),
                             (distance + x, y, TILE, TILE))

        if self.walls['top']:
            pygame.draw.line(screen, pygame.Color('black'), (distance + x, y), (distance + x + TILE, y), 2)
        if self.walls['right']:
            pygame.draw.line(screen, pygame.Color('black'), (distance + x + TILE, y), (distance + x + TILE, y + TILE), 2)
        if self.walls['bottom']:
            pygame.draw.line(screen, pygame.Color('black'), (distance + x + TILE, y + TILE), (distance + x, y + TILE), 2)
        if self.walls['left']:
            pygame.draw.line(screen, pygame.Color('black'), (distance + x, y + TILE), (distance + x, y), 2)

        if self.text != '0':
            if self.text[0] == 'A':
                text = font_use.render(self.text, True, (255, 0, 0))
                screen.blit(text, (distance + x + TILE / 2 - text.get_size()[0] / 2, y + TILE / 2 - text.get_size()[1] / 2))
            elif self.text[0] == 'T':
                text = font_use.render(self.text, True, (0, 0, 255))
                screen.blit(text, (distance + x + TILE / 2 - text.get_size()[0] / 2, y + TILE / 2 - text.get_size()[1] / 2))
            elif self.text[0] == 'K':
                text = font_use.render(self.text, True, (0, 255, 0))
                screen.blit(text, (distance + x + TILE / 2 - text.get_size()[0] / 2, y + TILE / 2 - text.get_size()[1] / 2))
            elif self.text[0] == 'D':
                if not self.visited:
                    pygame.draw.rect(screen, pygame.Color('grey'), (distance + x + 2, y + 2, TILE - 2, TILE - 2))
                text = font_use.render(self.text, True, (0, 0, 0))
                screen.blit(text, (distance + x + TILE / 2 - text.get_size()[0] / 2, y + TILE / 2 - text.get_size()[1] / 2))
            elif self.text == '-1' or self.text == "UP" or self.text == "DOWN":
                pygame.draw.rect(screen, pygame.Color('grey'), (distance + x + 2, y + 2, TILE - 2, TILE - 2))
                text = font_use.render(self.text, True, (0, 0, 0))
                screen.blit(text, (x + TILE / 2 - text.get_size()[0] / 2 + distance, y + TILE / 2 - text.get_size()[1] / 2))


every_map = map_read(map_game)


d, path = breadth_first_search(map_game)

N = len(map_game[0])
M = len(map_game[0][1])

RES = WIDTH, HEIGHT = M * TILE + 200, N * TILE
cols, rows = M, N

pygame.init()
sc = pygame.display.set_mode(RES)
pygame.display.set_caption("Move Your Step")

clock = pygame.time.Clock()
font = pygame.font.SysFont('sans', 15, True)

grid_cells = every_map[0]

dodai = len(path)
print(d)




i = 0
while True:
    sc.fill(pygame.Color('white'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if i < dodai:
        grid_cells = every_map[path[i][0]]
        if not grid_cells[path[i][2] + path[i][1] * cols].visited:
            grid_cells[path[i][2] + path[i][1] * cols].visited = True
        else:
            grid_cells[path[i][2] + path[i][1] * cols].color_intense *= 0.5
        i += 1

    if i >= dodai:
        num_floor = font.render(f'Floor: {path[dodai-1][0]+1}', True, (0, 0, 0))
        sc.blit(num_floor, (M * TILE + 10, 10))

        num_step = font.render(f'numbers step: {dodai-1}', True, (0, 0, 0))
        sc.blit(num_step, (M * TILE + 10, 40))

        # num_step = font.render(f'numbers step: {path[dodai-1][3]}', True, (0, 0, 0))
        # sc.blit(num_step, (M * TILE + 10, 70))
    else:
        num_floor = font.render(f'Floor: {path[i][0]+1}', True, (0, 0, 0))
        sc.blit(num_floor, (M * TILE + 10, 10))

        num_step = font.render(f'numbers step: {i}', True, (0, 0, 0))
        sc.blit(num_step, (M * TILE + 10, 40))

        # num_step = font.render(f'numbers key: {path[i][3]}', True, (0, 0, 0))
        # sc.blit(num_step, (M * TILE + 10, 70))

    [cell.draw(0, sc, font) for cell in grid_cells]

    pygame.display.flip()
    time.sleep(0.1)
    clock.tick(30)
