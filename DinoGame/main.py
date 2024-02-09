from machine import Pin, I2C
from games.dino.dino import Dino
from games.dino.cacti import Cacti
from games.dino.cloud import Cloud
from games.dino.checker import Checker
import display.ssd1306 as ssd1306

is_interrupt = False
start_game = False
game_over = False
first_jump = True
oled_widht = 128
oled_height = 64


def handle_interrupt(pin):
    global is_interrupt
    global start_game
    global game_over

    if game_over:
        game_over = False

    if start_game:
        is_interrupt = True

    if not game_over:
        start_game = True


button = Pin(2, mode=Pin.IN, pull=Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt)

i2c = I2C(1, sda=Pin(6), scl=Pin(7))
display = ssd1306.SSD1306_I2C(oled_widht, oled_height, i2c)

dino_obj = Dino(26, 26, 7, 38, 128)
cloud_obj = Cloud(32, 9, 48, 11, 128, 10)
cacti_obj_1 = Cacti(10, 24, 10, 18, 128, 39, 45, 20)
cacti_obj_2 = Cacti(10, 24, 10, 18, 128, 39, 45, 20)
checker_obj = Checker()


second_cacti = False

while True:
    display.fill(0)

    if game_over:
        display.fill(0)
        display.hline(0, 59, 127, 1)
        display.text("GAME OVER", 30, 20, 1)
        dino_obj.game_over(display)
        is_interrupt = False
        start_game = False
        second_cacti = False
        first_jump = True
        score = 0
        dino_obj.reset()
        cacti_obj_1.reset()
        cacti_obj_2.reset()
    elif not start_game:
        display.hline(0, 59, 127, 1)
        display.text("DINO RUN", 32, 20, 1)
        dino_obj.game_logo(display)
        is_interrupt = False
        second_cacti = False
    else:
        if first_jump:
            is_interrupt = False
            first_jump = False

        display.hline(0, 59, 127, 1)

        trigger_info = False

        trigger_info = cacti_obj_1.update(display)

        if trigger_info:
            cacti_obj_2.update(display)
            second_cacti = True

        if second_cacti:
            if (
                cacti_obj_2.size == 0
                and cacti_obj_2.current_x >= -cacti_obj_2.widht_big + 1
            ):
                cacti_obj_2.update(display)
            else:
                second_cacti == False

            if (
                cacti_obj_2.size == 1
                and cacti_obj_2.current_x >= -cacti_obj_2.widht_small + 1
            ):
                cacti_obj_2.update(display)
            else:
                second_cacti == False

        cloud_obj.update(display)
        dino_obj.update(display, 0)

        if is_interrupt:
            dino_obj.update(display, 1)
            is_interrupt = False

        cacti_obj_1.counter()
        cacti_obj_2.counter()

        score = cacti_obj_1.score + cacti_obj_2.score

        for cacti_obj in [cacti_obj_1, cacti_obj_2]:
            if cacti_obj.current_x < oled_widht / 1.5:
                if cacti_obj.size == 0:
                    game_over = checker_obj.check(
                        display,
                        dino_obj.width,
                        dino_obj.height,
                        dino_obj.current_x,
                        dino_obj.current_y,
                        cacti_obj.widht_big,
                        cacti_obj.height_big,
                        cacti_obj.current_x,
                        cacti_obj.current_y_big,
                    )
                elif cacti_obj.size == 1:
                    game_over = checker_obj.check(
                        display,
                        dino_obj.width,
                        dino_obj.height,
                        dino_obj.current_x,
                        dino_obj.current_y,
                        cacti_obj.widht_small,
                        cacti_obj.height_small,
                        cacti_obj.current_x,
                        cacti_obj.current_y_small,
                    )

        if game_over:
            start_game = False

        info = len(str(score))
        move = 106 - (8 * info)
        display.text("S:" + str(score), move, 5, 1)

    display.show()
