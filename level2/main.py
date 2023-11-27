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

RES = WIDTH, HEIGHT = M * TILE + 210 if (M * TILE + 210) < 1350 else 1350, N * TILE if N*TILE < 700 else 700
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
get_key = pygame.image.load("level2\keyget.png")
get_key = pygame.transform.scale(get_key,(20,20))
lost_key = pygame.image.load("level2\keylost.png")
lost_key = pygame.transform.scale(lost_key,(20,20))

dodai = len(path)

print(dodai)

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
                if (scrollx+1) * 25 < WIDTH and WIDTH > 1350:
                    scrollx += 1
            if event.key == pygame.K_LEFT:
                if scrollx > 0:
                    scrollx -= 1
            if event.key == pygame.K_DOWN and HEIGHT > 700:
                if (scrolly+1) * 25 < HEIGHT:
                    scrolly += 1
            if event.key == pygame.K_UP:
                if scrolly > 0:
                    scrolly -= 1

    if i < dodai:
        if not grid_cells[path[i][1] + path[i][0] * cols].visited:
            grid_cells[path[i][1] + path[i][0] * cols].visited = True
        else:
            grid_cells[path[i][1] + path[i][0] * cols].color_intense *= 0.5

        i += 1

    if i >= dodai:

        num_step = font.render(f'number of step: {dodai}', True, (0, 0, 0))
        sc.blit(num_step, (scrollx*25 + M * TILE + 10, scrolly*25 + 40))

        for num_key in range(len(path[dodai - 1][2])):
            dai = M * TILE + 10 + num_key * 20
            cao = 70
            if dai + 20 > WIDTH:
                dai -= 200 * int(num_key / 10)
                cao += 30 * int(num_key / 10)
            if path[dodai - 1][2][num_key] == '0':
                sc.blit(lost_key, (scrollx*25 + dai, scrolly*25 + cao))
            if path[dodai - 1][2][num_key] == '1':
                sc.blit(get_key, (scrollx*25 + dai, scrolly*25 + cao))

    else:

        num_step = font.render(f'number of steps: {i}', True, (0, 0, 0))
        sc.blit(num_step, (scrollx*25 + M * TILE + 10, scrolly*25 + 40))

        for num_key in range(len(path[i][2])):
            dai = M * TILE + 10 + num_key * 20
            cao = 70
            if dai + 20 > WIDTH:
                dai -= 200 * int(num_key / 10)
                cao += 30 * int(num_key / 10)
            if path[i][2][num_key] == '0':
                sc.blit(lost_key, (scrollx*25 + dai, scrolly*25 + cao))
            if path[i][2][num_key] == '1':
                sc.blit(get_key, (scrollx*25 + dai, scrolly*25 + cao))

    [cell.draw(scrollx*25, scrolly*25) for cell in grid_cells]

    pygame.display.flip()
    time.sleep(0.1)
    clock.tick(30)
