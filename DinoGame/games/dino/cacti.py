import framebuf
import random


class Cacti:
    def __init__(
        self,
        widht_big,
        height_big,
        widht_small,
        height_small,
        x,
        y_big,
        y_small,
        distance,
    ):
        self.widht_big = widht_big
        self.height_big = height_big
        self.widht_small = widht_small
        self.height_small = height_small
        self.x = x
        self.current_x = self.x
        self.y_big = y_big
        self.y_small = y_small
        self.current_y_big = self.y_big
        self.current_y_small = self.y_small
        self.size = 0
        self.area_percent = 35
        self.is_triggered = False
        self.distance = distance
        self.score = 0
        self.cacti_image_big = bytearray(
            b"\x0c\x00\x1e\x00\x1e\x00\x1e\x00\xde\x00\xde\x00\xde\x00\xde\xc0\xde\xc0\xfe\xc0\xfe\xc0\x7e\xc0\x1e\xc0\x1f\xc0\x1f\x80\x1e\x00\x1e\x00\x1e\x00\x1e\x00\x1e\x00\x1e\x00\x1e\x00\x1e\x00\x1e\x00"
        )
        self.cacti_image_small = bytearray(
            b"\x0e\x00\x1e\x00\x1e\x00\xde\x00\xde\x00\xde\xc0\xde\xc0\xfe\xc0\x7e\xc0\x1e\xc0\x1f\x80\x1e\x00\x1e\x00\x1e\x00\x1e\x00\x1e\x00\x1e\x00\x1e\x00"
        )

    def update(self, display):
        image_render_big = framebuf.FrameBuffer(
            self.cacti_image_big, self.widht_big, self.height_big, framebuf.MONO_HLSB
        )
        image_render_small = framebuf.FrameBuffer(
            self.cacti_image_small,
            self.widht_small,
            self.height_small,
            framebuf.MONO_HLSB,
        )

        if self.current_x <= -(self.widht_big - 1):
            self.size = random.randint(0, 1)
            self.current_x = self.x + self.distance
            self.is_triggered = False

        if self.size == 0:
            display.blit(image_render_big, self.current_x, self.current_y_big)
            self.current_x -= 1

        elif self.size == 1:
            display.blit(image_render_small, self.current_x, self.current_y_small)
            self.current_x -= 1

        if self.current_x - self.distance < self.x:
            if (
                ((100 * self.current_x) / self.x <= self.area_percent)
                and not self.is_triggered
                and ((100 * self.current_x) / self.x >= self.area_percent / 2)
            ):
                self.is_triggered = True
                return 1

    def counter(self):
        if self.current_x == 0:
            self.score += 1

    def reset(self):
        self.score = 0
        self.current_x = self.x
        self.is_triggered = False
