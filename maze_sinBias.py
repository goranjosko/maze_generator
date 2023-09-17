import pygame as pg
from pygame.locals import *
from math import sin, radians
from random import randint, choices, seed
from maze_font import TextFont
from maze_settings import *
from checking_error import ErrorHandler
import sys
import os


class Cell:
    size = CELLSIZE
    # line_size = 3

    def __init__(self, win, posx, posy, cell_id):
        # STATE shows whether the object has already been visited and determines the color
        self.state = 0
        # windows screen object used for drawing
        self.win = win
        self.posx = posx
        self.posy = posy
        self.size = CELLSIZE

        self.border_right = 1
        self.border_down = 1
        self.cell_id = cell_id
        self.background = 0
        self.stext = TextFont(13)
        self.start = False
        self.end = False

    # set borders false after waker pass over
    def set_border_right_false(self):
        self.border_right = False

    def set_border_down_false(self):
        self.border_down = False

    def draw(self, current=False):
        if current:
            pg.draw.rect(self.win, (107, 120, 150), (self.posx, self.posy,
                                                     self.size, self.size))
        else:
            if self.state == 1:
                self.background = COLOR_LIGHT
            elif self.state > 1:
                self.background = COLOR_DARK
            else:
                self.background = 0

            if self.background:
                pg.draw.rect(self.win, self.background, (self.posx, self.posy,
                                                         self.size, self.size))
            if self.start:
                pg.draw.circle(
                    self.win, COLOR_BLUE, (self.posx +
                                           CELLSIZE / 2, self.posy +
                                           CELLSIZE / 2), CELLSIZE / 2.4)
            elif self.end:
                pg.draw.circle(
                    self.win, COLOR_RED, (self.posx +
                                          CELLSIZE / 2, self.posy +
                                          CELLSIZE / 2), CELLSIZE / 2.4)

    def draw_borders(self):
        if self.border_right:
            pg.draw.line(self.win, ORANGE,
                         (self.posx + self.size, self.posy),
                         (self.posx + self.size, self.posy + self.size), width=BORDER_WDH)
        if self.border_down:
            pg.draw.line(self.win, ORANGE,
                         (self.posx, self.posy + self.size),
                         (self.posx + self.size, self.posy + self.size), width=BORDER_WDH)


class Walker:
    def __init__(self, start, h_cells):
        self.start = start
        self.h_cells = h_cells
        self.position = self.start
        self.queue = [self.position]
        self.i_pos = [0, 1, 2, 3]
        self.i_name = ['up', 'right', 'down', 'left']
        self.old_choice = ''
        self.maze_list = []
        self.maze_list_trigger = False
        self.sin_bias = 0
        self.sin_count = 0
        self.sin_count_up = True
        # self.created_debug()

    def calc_sin_bias(self):
        if self.sin_count_up:
            self.sin_count += 1
            if self.sin_count >= 180:
                self.sin_count_up = False
        else:
            self.sin_count -= 1
            if self.sin_count <= -180:
                self.sin_count_up = False

        def nrml(x):
            return round((x - 0) * 2 / 20)

        s = (
            round(float("{:.02f}".format(sin(radians(self.sin_count)) * 100))) // 2) + 50
        self.sin_bias = nrml(s)

    def created_debug(self):
        print('JUST CREATED AGAIN')

    def current_position(self):
        return self.position

    def last_sqare(self):
        return self.queue[-1]

    def next_position(self, temp, options, cells=[]):
        temp = [0 if x >= 0 else 1 for x in options]
        if self.old_choice:
            set_weights = self.ajust_weights(options)
        else:
            #  default weights setup for first move
            set_weights = [1 if x >= 0 else 0 for x in options]
        if all(temp):
            # all choices are negative...
            if self.maze_list_trigger:
                self.maze_list.append(self.queue.copy())
            cells[self.position].state += 1
            self.position = self.queue[-2]
            del self.queue[-1]
            self.maze_list_trigger = False
        else:
            random_choice = choices(
                self.i_pos, weights=set_weights, k=1)[0]

            self.position = options[random_choice]
            self.queue.append(self.position)
            self.clean_borders(random_choice, cells)
            self.old_choice = self.i_name[random_choice]
            self.maze_list_trigger = True

    def ajust_weights(self, options):
        set_weights = []
        if self.old_choice == 'up' or self.old_choice == 'down':
            for i, d in enumerate(options):
                if not i % 2:
                    if d >= 0:
                        set_weights.append(WBIAS_STRAIGHT + self.sin_bias)
                    else:
                        set_weights.append(0)
                else:
                    if d >= 0:
                        set_weights.append(WBIAS_MEANDERING)
                    else:
                        set_weights.append(0)
        elif self.old_choice == 'right' or self.old_choice == 'left':
            for i, d in enumerate(options):
                if i % 2:
                    if d >= 0:
                        set_weights.append(WBIAS_STRAIGHT + self.sin_bias)
                    else:
                        set_weights.append(0)
                else:
                    if d >= 0:
                        set_weights.append(WBIAS_MEANDERING)
                    else:
                        set_weights.append(0)
        return set_weights

    def clean_borders(self, random_choice, cells=[]):
        if self.i_name[random_choice] == 'up':
            cells[self.position].border_down = False
        elif self.i_name[random_choice] == 'right':
            cells[self.position - 1].border_right = False
        elif self.i_name[random_choice] == 'down':
            cells[self.position - self.h_cells].border_down = False
        elif self.i_name[random_choice] == 'left':
            cells[self.position].border_right = False


class Game:
    def __init__(self):
        pg.init()
        error = ErrorHandler()
        pg.display.set_caption(
            "SIMPLE BACKTRACKING RECRUZIVE ALGORITHM")
        error.value_check()
        width, height = TABLESIZE
        winwidth, winheight = WINSIZE
        self.win_screen = pg.display.set_mode(
            (winwidth, winheight), pg.HWSURFACE)
        self.maze = pg.Surface(
            (WINSIZE[0], TABLESIZE[1]))
        # self.maze_size = pg.display.set_mode((width, height), pg.HWSURFACE)
        screen_width, screen_height = pg.display.get_surface().get_size()
        # self.map_image = MAP_VIEW
        self.clock = pg.time.Clock()
        Game.exit = False
        # list of all cell objects in scene
        self.cell_list = []
        self.stext = TextFont(10)
        self.h_cells = int(self.maze.get_width() / Cell.size)
        self.v_cells = int(self.maze.get_height() / Cell.size)
        self.number_of_cells = self.h_cells * self.v_cells
        self.win_text = TextFont(19)
        # object that preform board walking
        self.walker = Walker(
            randint(0, self.number_of_cells - 1), self.h_cells)
        self.old_cell = self.walker.position

        self.evnt_nm = pg.USEREVENT + 1
        td = 10
        pg.time.set_timer(self.evnt_nm, td)

    def outside_brdrs(self):
        # up
        pg.draw.line(self.maze, ORANGE, (0, 0),
                     (TABLESIZE[0], 0), width=BORDER_WDH)
        # left
        pg.draw.line(self.maze, ORANGE, (0, 0),
                     (0, TABLESIZE[1]), width=BORDER_WDH)
        # down
        # pg.draw.line(self.maze, ORANGE, (0, TABLESIZE[1]),
        #              (TABLESIZE[0], TABLESIZE[1]), width=BORDER_WDH)
        # # right
        # pg.draw.line(self.maze, ORANGE, (TABLESIZE[0], 0),
        #              (TABLESIZE[0], TABLESIZE[1]), width=BORDER_WDH)

    # def sin_addition(self):
    #     self.walker.sin_bias

    def walk_options(self, pos):
        options = []
        #  first position up
        new_pos = pos - self.h_cells
        if pos >= self.h_cells and self.cell_list[new_pos].state == False:
            options.append(new_pos)
        else:
            options.append(-1)
        #  second position right
        new_pos = pos + 1
        if ((pos + 1) % self.h_cells != 0) and (pos < self.number_of_cells) and self.cell_list[new_pos].state == False:
            options.append(new_pos)
        else:
            options.append(-1)
        #  third position down
        new_pos = pos + self.h_cells
        if pos < self.number_of_cells - self.h_cells and self.cell_list[new_pos].state == False:
            options.append(new_pos)
        else:
            options.append(-1)
        #  fourth left
        new_pos = pos - 1
        if pos % self.h_cells != 0 and pos > 0 and self.cell_list[new_pos].state == False:
            options.append(new_pos)
        else:
            options.append(-1)
        # return [x if self.cell_list[x].state == False else -2 for x in options]
        return options

    def run(self):
        number = 0
        cell_id = 0
        cell_draw = True
        saved = False
        # make cells
        for j in range(self.v_cells):
            for i in range(self.h_cells):
                self.cell_list.append(Cell(self.maze, i * Cell.size,
                                      j * Cell.size, cell_id))
                cell_id += 1
                # self.cell_list[-1].draw()
        self.win_screen.fill((60, 40, 70))
        self.maze.fill((60, 40, 70))
        for c in self.cell_list:
            c.draw_borders()
        while not self.exit:
            event_list = pg.event.get()
            for event in event_list:
                event_holder = event
                pressed = pg.key.get_pressed()
                if event.type == pg.QUIT:
                    self.exit = True
                elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    pass
                elif event.type == self.evnt_nm:
                    self.walker.calc_sin_bias()

            # if we are in the drawing phase
            if cell_draw:

                # NEW "FASTER SYSTEM"
                if self.walker.position - 2 < 0:
                    rng_start = self.walker.position
                else:
                    rng_start = self.walker.position - 2
                if self.walker.position + 2 >= self.number_of_cells:
                    rng_end = self.walker.position
                else:
                    rng_end = self.walker.position + 2
                pos_list = []
                for i in range(rng_start, rng_end + 1):
                    pos_list.append(i)
                    if not i - self.h_cells < 0:
                        pos_list.append(i - self.h_cells)
                    if not i - self.h_cells * 2 < 0:
                        pos_list.append(i - self.h_cells * 2)
                    if not i + self.h_cells >= self.number_of_cells:
                        pos_list.append(i + self.h_cells)
                    if not i + self.h_cells * 2 >= self.number_of_cells:
                        pos_list.append(i + self.h_cells * 2)

                # current cell draw
                self.cell_list[self.walker.position].state += 1
                self.cell_list[self.walker.position].background = ORANGE
                self.cell_list[self.walker.position].draw(True)
                # old cell draw
                self.cell_list[self.old_cell].draw()

                for m in pos_list:
                    self.cell_list[m].draw_borders()
                # additional border on top and left because we draw only two borders per square
                self.outside_brdrs()
                # END OF NEW AND FASTER
                self.old_cell = self.walker.position
                self.win_screen.blit(self.maze, (0, 0))
                #  maze logic after drawing process is completed
                walk_options = self.walk_options(self.walker.position)
                walk_temp = [0 if x >= 0 else 1 for x in walk_options]

                self.walker.next_position(
                    walk_temp, walk_options, self.cell_list)

                if all(walk_temp):
                    if len(self.walker.queue) <= 1:
                        cell_draw = False

            # end of drawing phase, save file, display message
            else:
                self.walker.position = self.walker.last_sqare()
                solution = sorted(self.walker.maze_list,
                                  key=lambda x: len(x), reverse=True)[0][-1]
                # color and circle to start position
                self.cell_list[self.walker.position].state += 1
                self.cell_list[self.walker.start].start = True
                # add circle to solution cell
                self.cell_list[solution].end = True
                for i, cel in enumerate(self.cell_list):
                    cel.draw()

                for c in self.cell_list:
                    c.draw_borders()
                self.outside_brdrs()
                if not saved:
                    pg.image.save(self.maze, MAZE_IMAGE_FILE)
                    saved = True
                self.win_text.draw_text_box(self.maze, ((
                    self.h_cells * Cell.size) / 2 - 200, (self.v_cells * Cell.size) / 2, 400, 80), (255, 255, 255), 200, 15)
                self.win_text.draw_text(
                    self.maze, f'MAZE IS COMPLETED. /\nFILE SAVED AS {MAZE_IMAGE_FILE}',
                    ((self.h_cells * Cell.size) / 2 - 180, (self.v_cells * Cell.size) / 2 + 40), COLOR_RED)
                self.win_screen.blit(self.maze, (0, 0))
            # pg.display.flip()
            pg.display.update()

            self.clock.tick(FPS)
        pg.quit()

    def add_to_queue(self, item):
        if item not in self.queue:
            self.queue.append(item)
        else:
            try:
                print(f'dubble CELL: {item}')

            except Exception as error:
                print('Caught this error: ' + repr(error))


if __name__ == '__main__':
    game = Game()
    game.run()
