class Checker:
    def check(
        self,
        display,
        dino_widht,
        dino_height,
        dino_x,
        dino_y,
        cacti_widht,
        cacti_height,
        cacti_x,
        cacti_y,
    ):
        if (cacti_x <= dino_x+(dino_widht-3)) and (cacti_x+(cacti_widht-5) >= dino_x):
            if dino_y + (dino_height-2) >= cacti_y:
                return 1