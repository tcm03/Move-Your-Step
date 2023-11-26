import sys
import time
from random import choice
import pygame
from custom_parser import read_input
from bfs import breadth_first_search

map_game = read_input("level2\input1-level2.txt")

N = len(map_game)
M = len(map_game[0])

d, path = breadth_first_search(map_game)

TILE = 25
RES = WIDTH, HEIGHT = M * TILE , N * TILE
cols, rows = M, N

pygame.init()
sc = pygame.display.set_mode(RES)
pygame.display.set_caption("Move Your Step")

clock = pygame.time.Clock()
font = pygame.font.SysFont('sans', 15, True)


class Cell:
    def __init__(self, x, y, text='0', color_intense=1):
        self.x, self.y = x, y
        self.text = text
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.color_intense = color_intense

    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color('saddlebrown'), (x + 2, y + 2, TILE - 2, TILE - 2))

    def draw(self, distance):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, (
                int(255 * self.color_intense), int(255 * self.color_intense), int(153 * self.color_intense)),
                             (distance + x, y, TILE, TILE))

        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('black'), (distance + x, y), (distance + x + TILE, y), 2)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('black'), (distance + x + TILE, y), (distance + x + TILE, y + TILE), 2)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('black'), (distance + x + TILE, y + TILE), (distance + x, y + TILE), 2)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('black'), (distance + x, y + TILE), (distance + x, y), 2)

        if self.text != '0':
            if self.text[0] == 'A':
                text = font.render(self.text, True, (255, 0, 0))
                sc.blit(text, (distance + x + TILE / 2 - text.get_size()[0] / 2, y + TILE / 2 - text.get_size()[1] / 2))
            elif self.text[0] == 'T':
                text = font.render(self.text, True, (0, 0, 255))
                sc.blit(text, (distance + x + TILE / 2 - text.get_size()[0] / 2, y + TILE / 2 - text.get_size()[1] / 2))
            elif self.text[0] == 'K':
                text = font.render(self.text, True, (0, 255, 0))
                sc.blit(text, (distance + x + TILE / 2 - text.get_size()[0] / 2, y + TILE / 2 - text.get_size()[1] / 2))
            elif self.text[0] == 'D':
                if not self.visited:
                    pygame.draw.rect(sc, pygame.Color('grey'), (distance + x + 2, y + 2, TILE - 2, TILE - 2))
                text = font.render(self.text, True, (0, 0, 0))
                sc.blit(text, (distance + x + TILE / 2 - text.get_size()[0] / 2, y + TILE / 2 - text.get_size()[1] / 2))
            elif self.text == '-1' or self.text == "UP" or self.text == "DOWN":
                pygame.draw.rect(sc, pygame.Color('grey'), (distance + x + 2, y + 2, TILE - 2, TILE - 2))
                text = font.render(self.text, True, (0, 0, 0))
                sc.blit(text, (x + TILE / 2 - text.get_size()[0] / 2 + distance, y + TILE / 2 - text.get_size()[1] / 2))


grid_cells = [Cell(col, row, map_game[row][col]) for row in range(rows) for col in range(cols)]


dodai = len(path)

print(dodai)

i = 0
while True:
    sc.fill(pygame.Color('white'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if i < dodai:
        if not grid_cells[path[i][1] + path[i][0] * cols].visited:
            grid_cells[path[i][1] + path[i][0] * cols].visited = True
        else:
            grid_cells[path[i][1] + path[i][0] * cols].color_intense *= 0.5

        i += 1

    [cell.draw(0) for cell in grid_cells]

    pygame.display.flip()
    time.sleep(0.1)
    clock.tick(30)
