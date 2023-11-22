import sys
import time
from random import choice
import pygame
from custom_parser import read_input
from solver import breadth_first_search

map_game = read_input("input.txt")

N = len(map_game)
M = len(map_game[0])

d, path = breadth_first_search(map_game)

TILE = 25
RES = WIDTH, HEIGHT = M * TILE, N * TILE
cols, rows = M, N

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
font = pygame.font.SysFont('sans', 15, True)


class Cell:
    def __init__(self, x, y, text='0'):
        self.x, self.y = x, y
        self.text = text
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color('saddlebrown'), (x + 2, y + 2, TILE - 2, TILE - 2))

    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, (255,255,153), (x, y, TILE, TILE))

        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('black'), (x, y), (x + TILE, y), 2)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('black'), (x + TILE, y), (x + TILE, y + TILE), 2)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('black'), (x + TILE, y + TILE), (x, y + TILE), 2)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('black'), (x, y + TILE), (x, y), 2)

        if self.text != '0':
            if self.text[0] == 'A':
                text = font.render(self.text, True, (255, 0, 0))
                sc.blit(text, (x + TILE / 2 - text.get_size()[0] / 2, y + TILE / 2 - text.get_size()[1] / 2))
            elif self.text[0] == 'T':
                text = font.render(self.text, True, (0, 0, 255))
                sc.blit(text, (x + TILE / 2 - text.get_size()[0] / 2, y + TILE / 2 - text.get_size()[1] / 2))
            elif self.text[0] == 'K':
                text = font.render(self.text, True, (0, 255, 0))
                sc.blit(text, (x + TILE / 2 - text.get_size()[0] / 2, y + TILE / 2 - text.get_size()[1] / 2))
            elif self.text[0] == 'D':
                pygame.draw.rect(sc, pygame.Color('grey'), (x + 2, y + 2, TILE, TILE))
                text = font.render(self.text, True, (5, 255, 7))
                sc.blit(text, (x + TILE / 2 - text.get_size()[0] / 2, y + TILE / 2 - text.get_size()[1] / 2))
            elif self.text == '-1' or self.text == "UP" or self.text == "DOWN":
                pygame.draw.rect(sc, pygame.Color('grey'), (x + 2, y + 2, TILE, TILE))
                text = font.render(self.text, True, (0, 0, 0))
                sc.blit(text, (x + TILE / 2 - text.get_size()[0] / 2, y + TILE / 2 - text.get_size()[1] / 2))

    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]

    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False


grid_cells = [Cell(col, row, map_game[row][col]) for row in range(rows) for col in range(cols)]
# grid_cells[0].text = 'A1'
# current_cell = grid_cells[0]
# current_cell.visited = True
stack = []

dodai = len(path)

print(dodai)

for i in range(dodai):
    sc.fill(pygame.Color('white'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    grid_cells[path[i][1] + path[i][0] * cols].visited = True

    [cell.draw() for cell in grid_cells]

    pygame.display.flip()
    time.sleep(0.5)
    clock.tick(30)

print(path)

a = input("Stop")