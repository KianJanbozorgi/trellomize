import curses
from rich.console import Console
from typing import List, Optional

console = Console()


class Menu:
    """A class representing a simple menu using curses."""

    def __init__(self, items: List[str]):
        """Initialize the Menu class.

        Args:
            items (List[str]): The list of menu items. 
        """
        self.__items: List[str] = items
        self.__current_row: int = 1
        self.__max_row: int = len(items) - 1
        self.__selected_option: Optional[str] = None
        self.__enter_pressed: bool = False

    @property
    def selected_option(self) -> Optional[str]:
        """Returns the selected option."""
        return self.__selected_option

    @selected_option.setter
    def selected_option(self, selected_option):
        """Sets the selected option."""
        self.__selected_option = selected_option

    def display(self) -> None:
        """Display the menu."""
        self.__stdscr = curses.initscr()  # Initialize the curses screen
        curses.curs_set(0)  # Hide the cursor
        self.__stdscr.keypad(1)  # Enable special key inputs
        curses.start_color()  # Enable color support

        # Initialize color pairs
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

        while not self.__enter_pressed:
            self.__stdscr.clear()  # Clear the screen and draw the new menu
            for index, item in enumerate(self.__items):
                if index == self.__current_row:
                    self.__stdscr.addstr(
                        index, 0, item, curses.color_pair((index % 6) + 1))
                else:
                    self.__stdscr.addstr(index, 0, item)
            self.__stdscr.refresh()
            self.update_position()

    def update_position(self) -> None:
        """Updates the cursor position based on user input."""
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
            # If Enter key is pressed, mark the selected option
            self.__selected_option = self.__items[self.__current_row]
            self.__enter_pressed = True  # Flag to indicate that Enter key is pressed
            curses.endwin()  # Restore terminal settings
