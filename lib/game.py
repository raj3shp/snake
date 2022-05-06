import sys
import random
import curses

# Directions (X, Y) co-ordinates
UP = (0, 1)
DOWN = (0, -1)
# jump two columns for horizontal step
# to keep horizontal speed in proportion
# with vertical speed
LEFT = (-2, 0)
RIGHT = (2, 0)


def wrap_around(new_head, board_dimensions):
    h = board_dimensions[0]
    w = board_dimensions[1]
    if new_head[0] >= w - 1:
        new_head = (2, new_head[1])
    if new_head[0] <= 0:
        new_head = (w - 2, new_head[1])
    if new_head[1] >= h:
        new_head = (new_head[0], 1)
    if new_head[1] <= 0:
        new_head = (new_head[0], h - 1)
    return new_head

class Snake:
    def __init__(self, body, direction, bot_type=0):
        self.body = body
        self.direction = direction
        self.score = 0
        self.bot_type = bot_type

    def eat_apple(self, new_head, apple, direction):
        if direction in (LEFT, RIGHT) and apple.position in [new_head, (new_head[0] - 1, new_head[1])]:
            self.score += 1
            return True
        elif apple.position == new_head:
            self.score += 1
            return True
        return False

    def set_direction(self, key, size, apple):
        if key == curses.KEY_RIGHT and self.direction is not LEFT:
            self.take_step(RIGHT, size, apple)
        if key == curses.KEY_LEFT and self.direction is not RIGHT:
            self.take_step(LEFT, size, apple)
        if key == curses.KEY_DOWN and self.direction is not DOWN:
            self.take_step(UP, size, apple)
        if key == curses.KEY_UP and self.direction is not UP:
            self.take_step(DOWN, size, apple)

    def take_step(self, direction, board_dimensions, apple=None):
        self.direction = direction
        new_head = ((self.head()[0] + direction[0]), (self.head()[1] + direction[1]))

        new_head = wrap_around(new_head, board_dimensions)
        # If snake is not a no-collision bot
        if not self.bot_type == 1:
            # Game over, if new_head collides with body!
            if new_head in self.body:
                sys.exit("Game Over!\nScore: {}".format(self.score))

        if apple and self.eat_apple(new_head, apple, direction):
            apple.take_random_position(board_dimensions)
            self.body = self.body + [new_head]
        self.body = self.body[1:] + [new_head]

    def head(self):
        return self.body[-1]


class Apple:
    def __init__(self, position):
        self.position = position

    def take_random_position(self, board_dimensions):
        h = board_dimensions[0]
        w = board_dimensions[1]
        new_position = (random.randrange(1, (w - 2), 1), random.randrange(1, (h - 2), 1))
        # make sure x position is always even
        # we jump two columns for horizontal step
        if new_position[0] % 2 != 0:
            new_position = (new_position[0] + 1, new_position[1])
        self.position = wrap_around(new_position, board_dimensions)


class Game:
    def __init__(self, dimensions):
        self.height = dimensions[0]
        self.width = dimensions[1]

    def render(self, screen, snake, apple):
        """
        Render game using empty board:
        X represents snake head
        * represents snake body
        0 represents an apple
        """
        screen.addstr(0, 0, "+{}+".format("-" * (self.width - 2)))
        for y in range(1, self.height):
            row_str = "|"
            for x in range(1, self.width - 1):
                render_pos = (x, y)
                if render_pos in snake.body:
                    if render_pos == snake.head():
                        row_str += "O"
                    elif render_pos == snake.body[0]:
                        row_str += "+"
                    else:
                        row_str += "*"
                elif render_pos == apple.position:
                    row_str += "@"
                else:
                    row_str += " "
            screen.addstr(y, 0, row_str + "|")
        screen.addstr(self.height, 0, "+{}+".format("-" * (self.width - 2)))
        screen.addstr(self.height + 1, 0, "Score: {}".format(snake.score))
        return screen

