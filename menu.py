import curses
from rich.console import Console

console = Console()


class Menu:
    def __init__(self, items):
        self.__items = items
        self.__current_row = 1
        self.__max_row = len(items) - 1
        self.__selected_option = None
        self.__enter_pressed = False

    @property
    def selected_option(self):
        return self.__selected_option

    @selected_option.setter
    def selected_option(self, selected_option):
        self.__selected_option = selected_option

    def display(self):
        self.__stdscr = curses.initscr()
        curses.curs_set(0)
        self.__stdscr.keypad(1)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        while not self.__enter_pressed:
            self.__stdscr.clear()
            for index, item in enumerate(self.__items):
                if index == self.__current_row:
                    self.__stdscr.addstr(
                        index, 0, item, curses.color_pair((index % 6) + 1))
                else:
                    self.__stdscr.addstr(index, 0, item)
            self.__stdscr.refresh()
            self.update_position()

    def update_position(self):
        key = self.__stdscr.getch()
        if key == curses.KEY_UP:
            self.__current_row -= 1
            if self.__current_row < 1:
                self.__current_row = self.__max_row

        elif key == curses.KEY_DOWN:
            self.__current_row += 1
            if self.__current_row > self.__max_row:
                self.__current_row = 1

        elif key == 10:
            self.__selected_option = self.__items[self.__current_row]
            self.__enter_pressed = True
            curses.endwin()
