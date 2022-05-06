import time
import curses

from lib.game import Apple, Snake, Game, wrap_around
from lib.bot_joey import BotJoey
from lib.bot_isaac import BotIsaac
from lib.bot_elon import BotElon

# Directions (X, Y) co-ordinates
UP = (0, 1)
DOWN = (0, -1)
# jump two columns for horizontal step
# to keep horizontal speed in proportion
# with vertical speed
LEFT = (-2, 0)
RIGHT = (2, 0)

# Board dimensions (H, W)
SMALL_BOARD = (10, 30)
MEDIUM_BOARD = (20, 60)
BIG_BOARD = (30, 90)


def intro():
    intro_screen = """
                                 88                   
                                 88                   
                                 88                   
,adPPYba, 8b,dPPYba,  ,adPPYYba, 88   ,d8  ,adPPYba,  
I8[    "" 88P'   `"8a ""     `Y8 88 ,a8"  a8P_____88  
 `"Y8ba,  88       88 ,adPPPPP88 8888[    8PP"""""""  
aa    ]8I 88       88 88,    ,88 88`"Yba, "8b,   ,aa  
`"YbbdP"' 88       88 `"8bbdP"Y8 88   `Y8a `"Ybbd8"'  

    **Snake Game**

    Features:
     - Difficulty selection (1-20)
     - Select board size (1-3)
     - Auto-play with bot module

     Bot Types:
     1 Joey - Free run, no collision, basic
     2 Isaac - Simple collision avoidance pattern A
     3 Elon - Simple collision avoidance pattern B
    """
    print(intro_screen)
    refresh_rate = input("Enter speed (1-15) [5]: ")
    possible_speeds = [str(i) for i in range(1, 16)]
    if refresh_rate not in possible_speeds:
        refresh_rate = 5
    else:
        refresh_rate = int(refresh_rate)
    size = input("Enter board size (1-3) [2]: ")
    possible_sizes = [str(i) for i in range(1, 4)]
    if size not in possible_sizes:
        size = MEDIUM_BOARD
    else:
        size = int(size)
        if size == 1:
            size = SMALL_BOARD
        elif size == 2:
            size = MEDIUM_BOARD
        elif size == 3:
            size = BIG_BOARD

    possible_bots = [str(i) for i in range(1, 4)]
    bot_type = 0
    autoplay = input("Enable bot autoplay? (y/n) [n]: ")
    if autoplay == 'y':
        bot_type = input("Enter bot type (1-3) [1]: ")
        if bot_type in possible_bots:
            bot_type = int(bot_type)
        else:
            bot_type = 1
    return size, refresh_rate, bot_type


def main(screen, size, refresh_rate, bot_type):
    screen.clear()
    screen.nodelay(True)
    if bot_type == 0:
        snake = Snake([(1, 1), (1, 2), (1, 3)], LEFT)
    elif bot_type == 1:
        snake = BotJoey([(1, 1), (1, 2), (1, 3)], LEFT)
    elif bot_type == 2:
        snake = BotIsaac([(1, 1), (1, 2), (1, 3)], LEFT)
    elif bot_type == 3:
        snake = BotElon([(1, 1), (1, 2), (1, 3)], RIGHT)

    apple = Apple((3, 4))
    refresh_rate = (16 - refresh_rate) / 100

    game = Game(size)
    try:
        while True:
            if bot_type == 0:
                key = screen.getch()
                if key != -1:
                    snake.set_direction(key, size, apple)
                snake.take_step(snake.direction, size, apple)
            elif bot_type in [1, 2]:
                direction = snake.auto_play(apple)
                if direction:
                    snake.take_step(direction, size, apple)
            elif bot_type == 3:
                direction = snake.auto_play(apple)
                if direction:
                    new_head = (snake.head()[0] + snake.direction[0], snake.head()[1] + snake.direction[1])
                    new_head = wrap_around(new_head, size)
                    if new_head in snake.body:
                        direction = UP if direction in [LEFT, RIGHT] else LEFT
                        new_head = (snake.head()[0] + direction[0], snake.head()[1] + direction[1])
                        new_head = wrap_around(new_head, size)
                        if new_head in snake.body:
                            direction = DOWN if direction in [LEFT, RIGHT] else RIGHT
                    snake.set_direction(direction, size, apple)
            try:
                screen = game.render(screen, snake, apple)
                screen.refresh()
            except curses.error:
                exit("curses.error: ensure your terminal window is big enough to render {}x{}".format(size[0],
                                                                                                      size[1]))
            time.sleep(refresh_rate)
    except KeyboardInterrupt:
        exit("\nScore: {}\nSee ya!".format(snake.score))


if __name__ == "__main__":
    try:
        board_size, speed, bot = intro()
    except KeyboardInterrupt:
        exit("\nSee ya!")
    curses.wrapper(main, board_size, speed, bot)
