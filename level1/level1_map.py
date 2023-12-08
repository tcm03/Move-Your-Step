import os
import sys
import time
from random import choice
from tkinter import filedialog
import pygame
from level1.a_star import a_star
from level1.bfs import breadth_first_search

from level1.custom_parser import read_input
from level1.dfs import depth_first_search
from level1.dijkstra import dijkstra

import datetime
import tracemalloc


def level1_play(check):

    def openFile():
        filepath = ""
        while filepath == "":
            filepath = filedialog.askopenfilename(initialdir=".\level1",title="Choose the file",filetypes= (("text files","*.txt"),("all files","*.*")))
        return filepath

    filepath = openFile()

    map_game = read_input(filepath)

    N = len(map_game)
    M = len(map_game[0])

    d = None
    path = None
    record_list = None
    time_start = datetime.datetime.now()
    tracemalloc.start()
    if check == 1:
        d, path, record_list = a_star(map_game)
    elif check == 2:
        d, path, record_list = breadth_first_search(map_game)
    elif check == 3:
        d, path, record_list = depth_first_search(map_game)
    elif check == 4:
        d, path, record_list = dijkstra(map_game)
    current, peak = tracemalloc.get_traced_memory()
    time_end = datetime.datetime.now()
    tracemalloc.stop()
    

    TILE = 25
    FONTSIZE = 15
    
    
    WIDTH, HEIGHT = M * TILE + 210 if (M * TILE + 210) < 1350 else 1350, N * TILE if N*TILE < 700 else 700
    if HEIGHT < 200:
        HEIGHT = 200

    RES = WIDTH, HEIGHT

    cols, rows = M, N

    pygame.init()
    sc = pygame.display.set_mode(RES)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont('sans', FONTSIZE, True)

    if not os.path.isdir("level1\heatmap"):
        os.mkdir("level1\heatmap")
    class Cell:
        def __init__(self, x, y, text='0', color_intense=1):
            self.x, self.y = x, y
            self.text = text
            self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
            self.visited = False
            self.color_intense = color_intense

        def draw_current_cell(self,sc):
            x, y = self.x * TILE, self.y * TILE
            pygame.draw.rect(sc, pygame.Color('saddlebrown'), (x + 2, y + 2, TILE - 2, TILE - 2))

        def draw(self, distance, distancey,sc):
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
    
    def heat_map(record_list, N, M, map_game1, file_name):
        grid_cells1 = [Cell(col, row, map_game1[row][col]) for row in range(N) for col in range(M)]

        WIDTH1, HEIGHT1 = M * 25, N * 25

        RES1 = WIDTH1, HEIGHT1
        sc1 = pygame.display.set_mode(RES1)
        

        dodai = 0
        if record_list is not None:
            dodai = len(record_list)

        sc1.fill(pygame.Color('white'))

        for i in range(dodai):
            if not grid_cells1[record_list[i][1] + record_list[i][0] * cols].visited:
                grid_cells1[record_list[i][1] + record_list[i][0] * cols].visited = True
            else:
                grid_cells1[record_list[i][1] + record_list[i][0] * cols].color_intense *= 0.5

        [cell.draw(0 * 25, 0 * 25, sc1) for cell in grid_cells1]

        pygame.image.save(sc1, file_name+"visualize.png")
        
    def heat_map1(need_draw_map, N, M, file_name):

        WIDTH1, HEIGHT1 = M * 25, N * 25

        RES1 = WIDTH1, HEIGHT1
        sc1 = pygame.display.set_mode(RES1)
        sc1.fill(pygame.Color('white'))


        [cell.draw(0 * 25, 0 * 25, sc1) for cell in need_draw_map]

        pygame.image.save(sc1, file_name+"heatmap.png")


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
                now = datetime.datetime.now()
                t = now.strftime("%Y_%m_%d_%H_%M_%S")
                file_name = f'level1\heatmap\{t}\\'
                os.mkdir(file_name)
                TILE = 25
                heat_map(record_list,N,M,map_game,file_name)
                heat_map1(grid_cells,N, M, file_name)
                pygame.display.set_mode((800, 600))
                pygame.display.set_caption("Move Your Step")
                return True
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
            
            point = font.render(f"Points: {100-dodai}", True, (0, 0, 0))
            sc.blit(point, (scrollx*25 + M * TILE + 10, scrolly*25 + 70))
            
            memory_record = font.render(f"memory max: {round(peak / (1024 * 1024),3)} MB", True, (0, 0, 0))
            sc.blit(memory_record, (scrollx*25 + M * TILE + 10, scrolly*25 + 100))
            
            time_consume = font.render(f'time: {round((time_end - time_start).total_seconds() * 1000,3)} milliseconds', True, (0, 0, 0))
            sc.blit(time_consume, (scrollx*25 + M * TILE + 10, scrolly*25 + 130))

        else:

            num_step = font.render(f'number of steps: {i}', True, (0, 0, 0))
            sc.blit(num_step, (scrollx*25 + M * TILE + 10, scrolly*25 + 40))
            

        
        if path is None:
            solve_or_not = font.render('There are not any paths', True, (0, 0, 0))
            sc.blit(solve_or_not, (scrollx*25 + M * TILE + 10, scrolly*25 + 10))


        [cell.draw(scrollx*25, scrolly*25,sc) for cell in grid_cells]

        pygame.display.flip()
        time.sleep(0.1)
        clock.tick(30)