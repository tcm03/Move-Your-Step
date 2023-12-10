


import datetime
import os
import sys
import time
from tkinter import filedialog
import tracemalloc

import pygame

from level4.custom_parser import read_input
from level4.simulator import run_simulation


def level4_play(check):
    
    def openFile():
        filepath = ""
        while filepath == "":
            filepath = filedialog.askopenfilename(initialdir=".\\level4",title="Choose the file",filetypes= (("text files","*.txt"),("all files","*.*")))
        return filepath

    filepath = openFile()

    map_game = read_input(filepath)


    n_floor = len(map_game)


    def map_read(current, check = False):
        every_map = []
        for i in range(n_floor):
            map_i = current[i]
            current_map = [Cell(col, row,check, map_i[row][col]) for row in range(len(current[i])) for col in
                        range(len(current[i][0]))]
            every_map.append(current_map)
        return every_map


    TILE = 25
    FONTSIZE = 15


    class Cell:
        def __init__(self, x, y, check = False, text='0', color_old=(255, 255, 255), color_intense_list=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    agent_now=0, intense=1 ):
            self.x, self.y = x, y
            self.text = text
            self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
            self.visited = False
            self.color_old = color_old
            self.color_intense_list = color_intense_list.copy()
            self.agent_now = agent_now
            self.intense = intense
            self.check = check

        def changeText(self, text):
            self.text = text

        def draw(self, distance, distancey, screen, font_use):
            x, y = self.x * TILE, self.y * TILE
            if not self.check:
                if self.visited:
                    pygame.draw.rect(screen, (
                        int(self.color_old[0] * self.color_intense_list[self.agent_now]),
                        int(self.color_old[1] * self.color_intense_list[self.agent_now]),
                        int(self.color_old[2] * self.color_intense_list[self.agent_now])),
                                    (distance + x, distancey + y, TILE, TILE))
            else:
                if self.visited:
                    pygame.draw.rect(screen, (
                        int(self.color_old[0] * self.intense),
                        int(self.color_old[1] * self.intense),
                        int(self.color_old[2] * self.intense)),
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
                        distance + x + TILE / 2 - text.get_size()[0] / 2,
                        distancey + y + TILE / 2 - text.get_size()[1] / 2))
                elif self.text[0] == 'T':
                    text = font_use.render(self.text, True, (0, 0, 255))
                    screen.blit(text, (
                        distance + x + TILE / 2 - text.get_size()[0] / 2,
                        distancey + y + TILE / 2 - text.get_size()[1] / 2))
                elif self.text[0] == 'K':
                    text = font_use.render(self.text, True, (0, 255, 0))
                    screen.blit(text, (
                        distance + x + TILE / 2 - text.get_size()[0] / 2,
                        distancey + y + TILE / 2 - text.get_size()[1] / 2))
                elif self.text[0] == 'D':
                    if not self.visited:
                        pygame.draw.rect(screen, pygame.Color('grey'),
                                        (distance + x + 2, distancey + y + 2, TILE - 2, TILE - 2))
                    text = font_use.render(self.text, True, (0, 0, 0))
                    screen.blit(text, (
                        distance + x + TILE / 2 - text.get_size()[0] / 2,
                        distancey + y + TILE / 2 - text.get_size()[1] / 2))
                elif self.text == '-1' or self.text == "UP" or self.text == "DOWN":
                    pygame.draw.rect(screen, pygame.Color('grey'),
                                    (distance + x + 2, distancey + y + 2, TILE - 2, TILE - 2))
                    text = font_use.render(self.text, True, (0, 0, 0))
                    screen.blit(text, (
                        x + TILE / 2 - text.get_size()[0] / 2 + distance,
                        distancey + y + TILE / 2 - text.get_size()[1] / 2))


    every_map22 = map_read(map_game)

    time_start = datetime.datetime.now()
    tracemalloc.start()
    agent_path, target_list = run_simulation(map_game)
    current, peak = tracemalloc.get_traced_memory()
    time_end = datetime.datetime.now()
    tracemalloc.stop()
    

    N = len(map_game[0])
    M = len(map_game[0][1])

    WIDTH, HEIGHT = M * TILE + 210 if (M * TILE + 210) < 1350 else 1350, N * TILE if N * TILE < 700 else 700
    if HEIGHT < 200:
        HEIGHT = 200

    RES = WIDTH, HEIGHT

    cols, rows = M, N

    pygame.init()
    sc = pygame.display.set_mode(RES)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont('sans', FONTSIZE, True)

    grid_cells = every_map22[0]


    scrollx = 0
    scrolly = 0

    turn_agent = 0

    num_agent = 0

    num_path_agent1 = len(agent_path[1])
    check_exist = agent_path[1][num_path_agent1-1]
    kiemtra = map_game[check_exist[0]][check_exist[1]][check_exist[2]] == "T1"
    current_path_list = []
    check_stop_1 = 0

    for key, value in agent_path.items():
        num_agent += 1
        current_path_list.append(0)

    num_steps = 0
    
    if not os.path.isdir("level4\heatmap"):
        os.mkdir("level4\heatmap")


    agent_now = 0

    check_key = []
    for i in range(num_agent):
        check_key.append(0)


    def heatmap(record_list, n_floors, N, M, file_name, font, turn_agent_check, keylist):
        every_map1 = map_read(map_game, True)
        if record_list != None:
            for record in record_list:

                if not every_map1[record[0]][record[2] + record[1] * cols].visited:
                    every_map1[record[0]][record[2] + record[1] * cols].visited = True
                else:
                    every_map1[record[0]][record[2] + record[1] * cols].intense *= 0.5


                if turn_agent_check == 0:
                    every_map1[record[0]][record[2] + record[1] * cols].color_old = (255, 255, 153)
                elif turn_agent_check == 1:
                    every_map1[record[0]][record[2] + record[1] * cols].color_old = (244, 164, 96)
                elif turn_agent_check == 2:
                    every_map1[record[0]][record[2] + record[1] * cols].color_old = (204, 204, 255)
                elif turn_agent_check == 3:
                    every_map1[record[0]][record[2] + record[1] * cols].color_old = (255, 204, 229)
                elif turn_agent_check == 4:
                    every_map1[record[0]][record[2] + record[1] * cols].color_old = (204, 255, 204)
                elif turn_agent_check == 5:
                    every_map1[record[0]][record[2] + record[1] * cols].color_old = (204, 229, 255)
                elif turn_agent_check == 6:
                    every_map1[record[0]][record[2] + record[1] * cols].color_old = (204, 229, 255)
                elif turn_agent_check == 7:
                    every_map1[record[0]][record[2] + record[1] * cols].color_old = (229, 255, 204)
                elif turn_agent_check == 8:
                    every_map1[record[0]][record[2] + record[1] * cols].color_old = (255, 204, 204)

        for target in keylist[turn_agent_check+1]:
            every_map1[target[0]][target[2] + target[1] * cols].text = f"T{turn_agent_check+1}"

        WIDTH1, HEIGHT1 = M * 25, N * 25

        RES1 = WIDTH1, HEIGHT1
        sc1 = pygame.display.set_mode(RES1)
        sc1.fill(pygame.Color('white'))
        TILE = 25

        for i in range(n_floors):
            sc1.fill(pygame.Color('white'))
            [cell.draw(0 * 25, 0 * 25, sc1, font) for cell in every_map1[i]]

            pygame.image.save(sc1, file_name + f'floor{i + 1}.png')


    
    while True:
        sc.fill(pygame.Color('white'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                now = datetime.datetime.now()
                t = now.strftime("%Y_%m_%d_%H_%M_%S")
                file_name = f'level4\\heatmap\\{t}\\'
                os.mkdir(file_name)
                for num in range(num_agent):
                    file_name1 = file_name + f'agent{num + 1}\\'
                    os.mkdir(file_name1)
                    heatmap(agent_path[num + 1], n_floor, N, M, file_name1, font, num, target_list)
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
                    if TILE <= 23:
                        TILE += 2
                        if FONTSIZE <= 14:
                            FONTSIZE += 1
                        font = pygame.font.SysFont('sans', FONTSIZE, True)
        floor_check = None
        if check_stop_1 < num_path_agent1 and agent_path is not None and kiemtra:
            path = agent_path[(turn_agent + 1)]
            i = current_path_list[turn_agent]
            if i >= len(path):
                turn_agent = (turn_agent + 1) % num_agent
                continue
            grid_cells = every_map22[path[i][0]]
            grid_cells[path[i][2] + path[i][1] * cols].agent_now = turn_agent
            if not grid_cells[path[i][2] + path[i][1] * cols].visited:
                grid_cells[path[i][2] + path[i][1] * cols].visited = True
            else:
                grid_cells[path[i][2] + path[i][1] * cols].color_intense_list[turn_agent] *= 0.5

            f = target_list[turn_agent + 1][check_key[turn_agent]][0]
            x = target_list[turn_agent + 1][check_key[turn_agent]][1]
            y = target_list[turn_agent + 1][check_key[turn_agent]][2]
            test_change = False

            if target_list[turn_agent + 1][check_key[turn_agent]][0] == path[i][0] and target_list[turn_agent + 1][check_key[turn_agent]][1] == path[i][1] and target_list[turn_agent + 1][check_key[turn_agent]][2] == path[i][2]:
                if turn_agent != 0:
                    check_key[turn_agent] = check_key[turn_agent] + 1
                f = target_list[turn_agent + 1][check_key[turn_agent]][0]
                x = target_list[turn_agent + 1][check_key[turn_agent]][1]
                y = target_list[turn_agent + 1][check_key[turn_agent]][2]
                test_change = True

            if turn_agent == 0:
                grid_cells[path[i][2] + path[i][1] * cols].color_old = (255, 255, 153)
            elif turn_agent == 1:
                grid_cells[path[i][2] + path[i][1] * cols].color_old = (244, 164, 96)
            elif turn_agent == 2:
                grid_cells[path[i][2] + path[i][1] * cols].color_old = (204, 204, 255)
            elif turn_agent == 3:
                grid_cells[path[i][2] + path[i][1] * cols].color_old = (255, 204, 229)
            elif turn_agent == 4:
                grid_cells[path[i][2] + path[i][1] * cols].color_old = (204, 255, 204)
            elif turn_agent == 5:
                grid_cells[path[i][2] + path[i][1] * cols].color_old = (204, 229, 255)
            elif turn_agent == 6:
                grid_cells[path[i][2] + path[i][1] * cols].color_old = (204, 229, 255)
            elif turn_agent == 7:
                grid_cells[path[i][2] + path[i][1] * cols].color_old = (229, 255, 204)
            elif turn_agent == 8:
                grid_cells[path[i][2] + path[i][1] * cols].color_old = (255, 204, 204)

            if turn_agent == 0:
                check_stop_1 += 1
            num_steps += 1
            current_path_list[turn_agent] += 1
            agent_now = turn_agent
            
            floor_check = (f,x,y)

            if test_change is True:
                every_map22[path[i][0]][path[i][2] + path[i][1] * cols].changeText("0")

        if check_stop_1 >= num_path_agent1 and agent_path is not None and kiemtra:
            floor = agent_path[1][check_stop_1 - 1][0] + 1

            num_floor = font.render(f'Floor: {floor}', True, (0, 0, 0))
            sc.blit(num_floor, (scrollx * 25 + M * TILE + 10, scrolly * 25 + 10))

            agent_turn = font.render(f'Agent: {agent_now + 1}', True, (0, 0, 0))
            sc.blit(agent_turn, (scrollx * 25 + M * TILE + 10, scrolly * 25 + 30))

            num_step = font.render(f'number of steps: {num_steps}', True, (0, 0, 0))
            sc.blit(num_step, (scrollx * 25 + M * TILE + 10, scrolly * 25 + 50))

            point = font.render(f"Points: {100 - num_path_agent1}", True, (0, 0, 0))
            sc.blit(point, (scrollx * 25 + M * TILE + 10, scrolly * 25 + 70))

            memory_record = font.render(f"memory max: {round(peak / (1024 * 1024), 3)} MB", True, (0, 0, 0))
            sc.blit(memory_record, (scrollx * 25 + M * TILE + 10, scrolly * 25 + 90))

            time_consume = font.render(f'time: {round((time_end - time_start).total_seconds() * 1000, 3)} milliseconds',
                                    True, (0, 0, 0))
            sc.blit(time_consume, (scrollx * 25 + M * TILE + 10, scrolly * 25 + 110))
            
            

        elif agent_path is not None:
            path = agent_path[(turn_agent + 1)]
            i = current_path_list[turn_agent]
            num_floor = font.render(f'Floor: {path[i - 1][0] + 1}', True, (0, 0, 0))
            sc.blit(num_floor, (scrollx * 25 + M * TILE + 10, scrolly * 25 + 10))

            agent_turn = font.render(f'Agent: {agent_now + 1}', True, (0, 0, 0))
            sc.blit(agent_turn, (scrollx * 25 + M * TILE + 10, scrolly * 25 + 30))

            num_step = font.render(f'number of steps: {num_steps}', True, (0, 0, 0))
            sc.blit(num_step, (scrollx * 25 + M * TILE + 10, scrolly * 25 + 50))

        if kiemtra is False:
            solve_or_not = font.render('There are not any paths', True, (0, 0, 0))
            sc.blit(solve_or_not, (scrollx * 25 + M * TILE + 10, scrolly * 25 + 70))
            
        if floor_check is not None:
            every_map22[f][y + x * cols].changeText(f"T{turn_agent + 1}")

        [cell.draw(scrollx * 25, scrolly * 25, sc, font) for cell in grid_cells]
        turn_agent = (turn_agent + 1) % num_agent

        pygame.display.flip()
        time.sleep(0.2)
        clock.tick(30)
