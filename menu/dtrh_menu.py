import curses
import logging

class DynamicMenu:
    def __init__(self, stdscr, config):
        self.stdscr = stdscr
        self.config = config
        self.menu_stack = [self.config['items']]
        self.current_menu = self.menu_stack[-1]
        self.current_index = 0

    def draw_menu(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        for idx, item in enumerate(self.current_menu):
            x = w//2 - len(item['title'])//2
            y = h//2 - len(self.current_menu)//2 + idx
            if idx == self.current_index:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, item['title'])
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, item['title'])
        self.stdscr.refresh()

    def run(self):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        while True:
            self.draw_menu()
            key = self.stdscr.getch()
            if key in [curses.KEY_UP, ord('k')]:
                self.current_index = (self.current_index - 1) % len(self.current_menu)
            elif key in [curses.KEY_DOWN, ord('j')]:
                self.current_index = (self.current_index + 1) % len(self.current_menu)
            elif key in [curses.KEY_RIGHT, ord('d'), curses.KEY_ENTER, ord('\n')]:
                self.select_item()
            elif key in [curses.KEY_LEFT, ord('a'), 27]:  # 27 is ESC
                self.go_back()
            elif key in [ord('q'), 3]:  # 3 is Ctrl+C
                break

    def select_item(self):
        selected_item = self.current_menu[self.current_index]
        if 'submenu' in selected_item:
            self.menu_stack.append(selected_item['submenu'])
            self.current_menu = self.menu_stack[-1]
            self.current_index = 0
        elif 'action' in selected_item:
            self.perform_action(selected_item['action'])

    def go_back(self):
        if len(self.menu_stack) > 1:
            self.menu_stack.pop()
            self.current_menu = self.menu_stack[-1]
            self.current_index = 0

    def perform_action(self, action):
        logging.info(f"Performing action: {action}")
        if action == 'exit':
            curses.endwin()
            exit()
        # Define other actions here
