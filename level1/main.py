import sys
import time
from random import choice
import pygame
from custom_parser import read_input
from dfs import depth_first_search

map_game = read_input("../input/input1-level1.txt")

N = len(map_game)
M = len(map_game[0])


d, path = depth_first_search(map_game)

TILE = 25
FONTSIZE = 15

RES = WIDTH, HEIGHT = M * TILE + 210 if (M * TILE + 210) < 1350 else 1350, N * TILE if N*TILE < 700 else 700
cols, rows = M, N

pygame.init()
sc = pygame.display.set_mode(RES)
pygame.display.set_caption("Move Your Step")

clock = pygame.time.Clock()
font = pygame.font.SysFont('sans', FONTSIZE, True)


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

    def draw(self, distance, distancey):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, (
                int(255 * self.color_intense), int(255 * self.color_intense), int(153 * self.color_intense)),
                             (distance + x, distancey + y, TILE, TILE))

        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('black'), (distance + x,distancey + y), (distance + x + TILE, distancey + y), 2)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('black'), (distance + x + TILE,distancey + y), (distance + x + TILE, distancey + y + TILE), 2)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('black'), (distance + x + TILE,distancey + y + TILE), (distance + x,distancey + y + TILE), 2)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('black'), (distance + x,distancey + y + TILE), (distance + x,distancey + y), 2)

        if self.text != '0':
            if self.text[0] == 'A':
                text = font.render(self.text, True, (255, 0, 0))
                sc.blit(text, (distance + x + TILE / 2 - text.get_size()[0] / 2,distancey + y + TILE / 2 - text.get_size()[1] / 2))
            elif self.text[0] == 'T':
                text = font.render(self.text, True, (0, 0, 255))
                sc.blit(text, (distance + x + TILE / 2 - text.get_size()[0] / 2,distancey + y + TILE / 2 - text.get_size()[1] / 2))
            elif self.text[0] == 'K':
                text = font.render(self.text, True, (0, 255, 0))
                sc.blit(text, (distance + x + TILE / 2 - text.get_size()[0] / 2,distancey + y + TILE / 2 - text.get_size()[1] / 2))
            elif self.text[0] == 'D':
                if not self.visited:
                    pygame.draw.rect(sc, pygame.Color('grey'), (distance + x + 2,distancey + y + 2, TILE - 2, TILE - 2))
                text = font.render(self.text, True, (0, 0, 0))
                sc.blit(text, (distance + x + TILE / 2 - text.get_size()[0] / 2,distancey + y + TILE / 2 - text.get_size()[1] / 2))
            elif self.text == '-1' or self.text == "UP" or self.text == "DOWN":
                pygame.draw.rect(sc, pygame.Color('grey'), (distance + x + 2,distancey + y + 2, TILE - 2, TILE - 2))
                text = font.render(self.text, True, (0, 0, 0))
                sc.blit(text, (x + TILE / 2 - text.get_size()[0] / 2 + distance,distancey + y + TILE / 2 - text.get_size()[1] / 2))


grid_cells = [Cell(col, row, map_game[row][col]) for row in range(rows) for col in range(cols)]


dodai = 0
if path is not None:
    dodai = len(path)



scrollx = 0
scrolly = 0

i = 0
while True:
    sc.fill(pygame.Color('white'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                scrollx += 1
            if event.key == pygame.K_LEFT:
                scrollx -= 1
            if event.key == pygame.K_DOWN:
                scrolly += 1
            if event.key == pygame.K_UP:
                scrolly -= 1
            if event.key == pygame.K_z:
                if TILE >= 3:
                    TILE -= 2
                    if FONTSIZE >= 2:
                        FONTSIZE -= 1
                    font = pygame.font.SysFont('sans', FONTSIZE, True)
            if event.key == pygame.K_x:
                if TILE <= 23 :
                    TILE += 2
                    if FONTSIZE <=14:
                        FONTSIZE += 1
                    font = pygame.font.SysFont('sans', FONTSIZE, True)

    if i < dodai:
        if not grid_cells[path[i][1] + path[i][0] * cols].visited:
            grid_cells[path[i][1] + path[i][0] * cols].visited = True
        else:
            grid_cells[path[i][1] + path[i][0] * cols].color_intense *= 0.5

        i += 1

    if i >= dodai:

        num_step = font.render(f'number of step: {dodai}', True, (0, 0, 0))
        sc.blit(num_step, (scrollx*25 + M * TILE + 10, scrolly*25 + 40))

    else:

        num_step = font.render(f'number of steps: {i}', True, (0, 0, 0))
        sc.blit(num_step, (scrollx*25 + M * TILE + 10, scrolly*25 + 40))
    
    if path is None:
        solve_or_not = font.render('There are not any paths', True, (0, 0, 0))
        sc.blit(solve_or_not, (scrollx*25 + M * TILE + 10, scrolly*25 + 10))


    [cell.draw(scrollx*25, scrolly*25) for cell in grid_cells]

    pygame.display.flip()
    time.sleep(0.1)
    clock.tick(30)