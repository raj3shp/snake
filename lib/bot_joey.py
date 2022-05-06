from lib.game import Snake, LEFT, RIGHT, UP, DOWN

class BotJoey(Snake):
    def __init__(self, body, direction, bot_type=1):
        super().__init__(body, direction, bot_type)

    def auto_play(self, apple):
        """
        Very basic logic, does not consider
        snake colliding into it's own body

        Snake class's take_step method has
        special handling for this bot level
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
            if head_y <= apple_y:
                return self.direction
            else:
                return DOWN
        if self.direction == DOWN:
            if head_y >= apple_y:
                return self.direction
            else:
                return UP
        if self.direction == LEFT:
            if head_x >= apple_x:
                return self.direction
            else:
                return RIGHT
        if self.direction == RIGHT:
            if head_x <= apple_x:
                return self.direction
            else:
                return LEFT
