from lib.game import Snake, LEFT, RIGHT, UP, DOWN

class BotElon(Snake):
    def __init__(self, body, direction, bot_type=3):
        super().__init__(body, direction, bot_type)

    def set_direction(self, direction, size, apple):
        if direction == RIGHT and self.direction is not LEFT:
            self.take_step(RIGHT, size, apple)
        if direction == LEFT and self.direction is not RIGHT:
            self.take_step(LEFT, size, apple)
        if direction == DOWN and self.direction is not DOWN:
            self.take_step(UP, size, apple)
        if direction == UP and self.direction is not UP:
            self.take_step(DOWN, size, apple)

    def auto_play(self, apple):
        """
        Smarter than Isaac, does
        the same thing in less code and
        produces weird pattern
        """

        head_x = self.head()[0]
        head_y = self.head()[1]
        apple_x = apple.position[0]
        apple_y = apple.position[1]
        if apple_y != head_y:
            if apple_y > head_y:
                return DOWN if self.direction is not UP else LEFT
            else:
                return UP if self.direction is not DOWN else RIGHT
        elif apple_x != head_x:
            if apple_x > head_x:
                return RIGHT if self.direction is not LEFT else DOWN
            else:
                return LEFT if self.direction is not RIGHT else UP

