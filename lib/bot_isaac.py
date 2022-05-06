from lib.game import Snake, LEFT, RIGHT, UP, DOWN

class BotIsaac(Snake):
    def __init__(self, body, direction, bot_type=2):
        super().__init__(body, direction, bot_type)

    def auto_play(self, apple):
        """
        A bit smarter than joey, tries to
        avoid colliding into it's own body
        """
        head_x = self.head()[0]
        head_y = self.head()[1]
        apple_x = apple.position[0]
        apple_y = apple.position[1]
        if head_y == apple_y:
            return LEFT
        if head_x == apple_x:
            return UP
        if self.direction == UP:
            if head_x <= apple_x:
                return RIGHT
            if head_x >= apple_x:
                return LEFT
            if head_y <= apple_y:
                return self.direction
            else:
                return LEFT
        if self.direction == DOWN:
            if head_x >= apple_x:
                return LEFT
            if head_x <= apple_x:
                return RIGHT
            if head_y >= apple_y:
                return self.direction
            else:
                return LEFT
        if self.direction == LEFT:
            if head_y >= apple_y:
                return DOWN
            if head_y <= apple_y:
                return UP
            if head_x >= apple_x:
                return self.direction
            else:
                return UP
        if self.direction == RIGHT:
            if head_x <= apple_x:
                return DOWN
            if head_x >= apple_x:
                return UP
            if head_x <= apple_x:
                return self.direction
            else:
                return DOWN
