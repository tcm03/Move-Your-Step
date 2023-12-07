import datetime
import os
import sys
import time
from random import choice
from tkinter import filedialog
import tracemalloc
import pygame
from level3.bfs import breadth_first_search

from level3.custom_parser import read_input
from level3.dfs import depth_first_search
from level3.dijkstra import dijkstra



def level3_play(check):
    
    def openFile():
        filepath = ""
        while filepath == "":
            filepath = filedialog.askopenfilename(initialdir=".\level3",title="Choose the file",filetypes= (("text files","*.txt"),("all files","*.*")))
        return filepath

    filepath = openFile()

    map_game = read_input(filepath)

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
    FONTSIZE = 15
    
    if not os.path.isdir("level3\heatmap"):
        os.mkdir("level3\heatmap")


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

        def draw(self, distance, distancey, screen, font_use):
            x, y = self.x * TILE, self.y * TILE
            if self.visited:
                pygame.draw.rect(screen, (
                    int(255 * self.color_intense), int(255 * self.color_intense), int(153 * self.color_intense)),
                                (distance + x, distancey + y, TILE, TILE))

            if self.walls['top']:
                pygame.draw.line(screen, pygame.Color('black'), (distance + x, distancey + y),
                                (distance + x + TILE, distancey + y), 2)
            if self.walls['right']:
                pygame.draw.line(screen, pygame.Color('black'), (distance + x + TILE, distancey + y),
                                (distance + x + TILE, distancey + y + TILE), 2)
            if self.walls['bottom']:
                pygame.draw.line(screen, pygame.Color('black'), (distance + x + TILE, distancey + y + TILE),
                                (distance + x, distancey + y + TILE), 2)
            if self.walls['left']:
                pygame.draw.line(screen, pygame.Color('black'), (distance + x, distancey + y + TILE),
                                (distance + x, distancey + y), 2)

            if self.text != '0':
                if self.text[0] == 'A':
                    text = font_use.render(self.text, True, (255, 0, 0))
                    screen.blit(text, (
                    distance + x + TILE / 2 - text.get_size()[0] / 2, distancey + y + TILE / 2 - text.get_size()[1] / 2))
                elif self.text[0] == 'T':
                    text = font_use.render(self.text, True, (0, 0, 255))
                    screen.blit(text, (
                    distance + x + TILE / 2 - text.get_size()[0] / 2, distancey + y + TILE / 2 - text.get_size()[1] / 2))
                elif self.text[0] == 'K':
                    text = font_use.render(self.text, True, (0, 255, 0))
                    screen.blit(text, (
                    distance + x + TILE / 2 - text.get_size()[0] / 2, distancey + y + TILE / 2 - text.get_size()[1] / 2))
                elif self.text[0] == 'D':
                    if not self.visited:
                        pygame.draw.rect(screen, pygame.Color('grey'),
                                        (distance + x + 2, distancey + y + 2, TILE - 2, TILE - 2))
                    text = font_use.render(self.text, True, (0, 0, 0))
                    screen.blit(text, (
                    distance + x + TILE / 2 - text.get_size()[0] / 2, distancey + y + TILE / 2 - text.get_size()[1] / 2))
                elif self.text == '-1' or self.text == "UP" or self.text == "DOWN":
                    pygame.draw.rect(screen, pygame.Color('grey'),
                                    (distance + x + 2, distancey + y + 2, TILE - 2, TILE - 2))
                    text = font_use.render(self.text, True, (0, 0, 0))
                    screen.blit(text, (
                    x + TILE / 2 - text.get_size()[0] / 2 + distance, distancey + y + TILE / 2 - text.get_size()[1] / 2))


    every_map = map_read(map_game)
    
    d = None
    path = None
    record_list = None
    
    time_start = datetime.datetime.now()
    tracemalloc.start()
    if check == 1:
        d, path, record_list = dijkstra(map_game)
    elif check == 2:
        d, path, record_list = breadth_first_search(map_game)
    elif check == 3:
        d, path, record_list = depth_first_search(map_game)
    current, peak = tracemalloc.get_traced_memory()
    time_end = datetime.datetime.now()
    tracemalloc.stop()

    def heatmap(record_list,n_floors, N, M, file_name, font):
        
        every_map1 = map_read(map_game)
        if record_list != None:
            for record in record_list:

                if not every_map1[record[0]][record[2] + record[1] * cols].visited:
                    every_map1[record[0]][record[2] + record[1] * cols].visited = True
                else:
                    every_map1[record[0]][record[2] + record[1] * cols].color_intense *= 0.5

        WIDTH1, HEIGHT1 = M * 25, N * 25

        RES1 = WIDTH1, HEIGHT1
        sc1 = pygame.display.set_mode(RES1)
        
        TILE = 25

        for i in range(n_floors):
            sc1.fill(pygame.Color('white'))

            [cell.draw(0 * 25, 0 * 25, sc1, font) for cell in every_map1[i]]

            pygame.image.save(sc1, file_name+f'floor{i+1}.png')
            
    def heatmap1(every_map1, n_floors, N, M, file_name):
        WIDTH1, HEIGHT1 = M * 25, N * 25

        RES1 = WIDTH1, HEIGHT1
        sc2 = pygame.display.set_mode(RES1)
        sc2.fill(pygame.Color('white'))
        TILE = 25

        for i in range(n_floors):
            sc2.fill(pygame.Color('white'))

            [cell.draw(0 * 25, 0 * 25, sc2, font) for cell in every_map1[i]]

            pygame.image.save(sc2, file_name+f'floor{i+1}.png')

    N = len(map_game[0])
    M = len(map_game[0][1])
    
    WIDTH, HEIGHT = M * TILE + 210 if (M * TILE + 210) < 1350 else 1350, N * TILE if N*TILE < 700 else 700
    if HEIGHT < 200:
        HEIGHT = 200

    RES = WIDTH, HEIGHT

    cols, rows = M, N

    pygame.init()
    sc = pygame.display.set_mode(RES)
    pygame.display.set_caption("BFS")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont('sans', FONTSIZE, True)

    grid_cells = every_map[0]


    get_key = pygame.image.load("level3\keyget.png")
    get_key = pygame.transform.scale(get_key, (20, 20))
    lost_key = pygame.image.load("level3\keylost.png")
    lost_key = pygame.transform.scale(lost_key, (20, 20))

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
                file_name = f'level3\heatmap\{t}\\'
                os.mkdir(file_name)
                visualizedir = file_name + "heatmap\\" 
                os.mkdir(visualizedir)
                heatmap1(every_map,n_floor, N, M, visualizedir)
                heatmapdir = file_name + "visualize\\"
                os.mkdir(heatmapdir)
                heatmap(record_list,n_floor,N,M,heatmapdir,font)
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
        if i < dodai and path is not None:
            grid_cells = every_map[path[i][0]]
            if not grid_cells[path[i][2] + path[i][1] * cols].visited:
                grid_cells[path[i][2] + path[i][1] * cols].visited = True
            else:
                grid_cells[path[i][2] + path[i][1] * cols].color_intense *= 0.5
            i += 1

        if i >= dodai and path is not None:
            
            
            num_floor = font.render(f'Floor: {path[dodai - 1][0] + 1}', True, (0, 0, 0))
            sc.blit(num_floor, (scrollx * 25 + M * TILE + 10, scrolly * 25 + 10))

            num_step = font.render(f'number of steps: {dodai}', True, (0, 0, 0))
            sc.blit(num_step, (scrollx * 25 + M * TILE + 10, scrolly * 25 + 40))
            
            point = font.render(f"Points: {100-dodai}", True, (0, 0, 0))
            sc.blit(point, (scrollx*25 + M * TILE + 10, scrolly*25 + 70))
            
            memory_record = font.render(f"memory max: {round(peak / (1024 * 1024),3)} MB", True, (0, 0, 0))
            sc.blit(memory_record, (scrollx*25 + M * TILE + 10, scrolly*25 + 100))
            
            time_consume = font.render(f'time: {round((time_end - time_start).total_seconds() * 1000,3)} milliseconds', True, (0, 0, 0))
            sc.blit(time_consume, (scrollx*25 + M * TILE + 10, scrolly*25 + 130))
            
            
            

            for num_key in range(len(path[dodai - 1][3])):
                dai = M * TILE + 10 + num_key * 20
                cao = 160
                if dai + 20 > WIDTH:
                    dai -= 200 * int(num_key / 10)
                    cao += 30 * int(num_key / 10)
                if path[dodai - 1][3][num_key] == '0':
                    sc.blit(lost_key, (scrollx * 25 + dai, scrolly * 25 + cao))
                if path[dodai - 1][3][num_key] == '1':
                    sc.blit(get_key, (scrollx * 25 + dai, scrolly * 25 + cao))
                    
            

            # num_step = font.render(f'numbers step: {path[dodai-1][3]}', True, (0, 0, 0))
            # sc.blit(num_step, (M * TILE + 10, 70))
        elif path is not None:
            num_floor = font.render(f'Floor: {path[i][0] + 1}', True, (0, 0, 0))
            sc.blit(num_floor, (scrollx * 25 + M * TILE + 10, scrolly * 25 + 10))

            num_step = font.render(f'number of steps: {i}', True, (0, 0, 0))
            sc.blit(num_step, (scrollx * 25 + M * TILE + 10, scrolly * 25 + 40))

            for num_key in range(len(path[i][3])):
                dai = M * TILE + 10 + num_key * 20
                cao = 70
                if dai + 20 > WIDTH:
                    dai -= 200 * int(num_key / 10)
                    cao += 30 * int(num_key / 10)
                if path[i][3][num_key] == '0':
                    sc.blit(lost_key, (scrollx * 25 + dai, scrolly * 25 + cao))
                if path[i][3][num_key] == '1':
                    sc.blit(get_key, (scrollx * 25 + dai, scrolly * 25 + cao))
                    
        if path is None:
            solve_or_not = font.render('There are not any paths', True, (0, 0, 0))
            sc.blit(solve_or_not, (scrollx*25 + M * TILE + 10, scrolly*25 + 10))

        [cell.draw(scrollx * 25, scrolly * 25, sc, font) for cell in grid_cells]
        

        pygame.display.flip()
        time.sleep(0.1)
        clock.tick(30)
