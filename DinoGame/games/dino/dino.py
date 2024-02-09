import framebuf


class Dino:
    def __init__(self, width, height, x, y, max_screen_size):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.current_x = self.x
        self.current_y = self.y
        self.state = 0  # 0 in no jump, 1 in jump up, 2 in jump down
        self.legs_counter_index = 13
        self.legs_counter = 0
        self.top_slower_index = 22
        self.top_slower = 0
        self.max_screen_size = max_screen_size
        self.dino_image = bytearray(
            b"\x00\x07\xff\x00\x00\x0c\x7f\x80\x00\x0c\x7f\x80\x00\x0c\xff\x80\x00\x0f\xff\x80\x00\x0f\xff\x80\x00\x0f\xff\x80\x00\x0f\xc0\x00\x00\x0f\xc0\x00\x00\x0f\xfe\x00\x40\x3f\xc0\x00\x40\x7f\xc0\x00\x60\xff\xc0\x00\x60\xff\xc0\x00\x71\xff\xf0\x00\x7f\xff\xd0\x00\x7f\xff\xc0\x00\x3f\xff\xc0\x00\x3f\xff\xc0\x00\x1f\xff\x80\x00\x0f\xfe\x00\x00\x03\xec\x00\x00\x01\xc4\x00\x00\x01\x84\x00\x00\x01\x04\x00\x00\x01\x86\x00\x00"
        )
        self.dino_right_leg_image = bytearray(
            b"\x00\x07\xff\x00\x00\x0c\x7f\x80\x00\x0c\x7f\x80\x00\x0c\xff\x80\x00\x0f\xff\x80\x00\x0f\xff\x80\x00\x0f\xff\x80\x00\x0f\xc0\x00\x00\x0f\xc0\x00\x00\x0f\xfe\x00\x40\x3f\xc0\x00\x40\x7f\xc0\x00\x60\xff\xc0\x00\x60\xff\xc0\x00\x71\xff\xf0\x00\x7f\xff\xd0\x00\x7f\xff\xc0\x00\x3f\xff\xc0\x00\x3f\xff\xc0\x00\x1f\xff\x80\x00\x0f\xfe\x00\x00\x03\xec\x00\x00\x01\xc6\x00\x00\x01\x86\x00\x00\x01\x00\x00\x00\x01\x80\x00\x00"
        )
        self.dino_left_leg_image = bytearray(
            b"\x00\x07\xff\x00\x00\x0c\x7f\x80\x00\x0c\x7f\x80\x00\x0c\xff\x80\x00\x0f\xff\x80\x00\x0f\xff\x80\x00\x0f\xff\x80\x00\x0f\xc0\x00\x00\x0f\xc0\x00\x00\x0f\xfe\x00\x40\x3f\xc0\x00\x40\x7f\xc0\x00\x60\xff\xc0\x00\x60\xff\xc0\x00\x71\xff\xf0\x00\x7f\xff\xd0\x00\x7f\xff\xc0\x00\x3f\xff\xc0\x00\x3f\xff\xc0\x00\x1f\xff\x80\x00\x0f\xfe\x00\x00\x03\xec\x00\x00\x01\xc4\x00\x00\x01\x84\x00\x00\x01\x84\x00\x00\x00\x06\x00\x00"
        )
        self.dino_image_dead = bytearray(
            b"\x00\x07\xff\x00\x00\x0c\x7f\x80\x00\x0d\x7f\x80\x00\x0c\x7f\x80\x00\x0f\xff\x80\x00\x0f\xff\x80\x00\x0f\xff\x80\x00\x0f\xff\x80\x00\x0f\xff\x80\x00\x0f\xfe\x00\x40\x3f\xc0\x00\x40\x7f\xc0\x00\x60\xff\xc0\x00\x60\xff\xc0\x00\x71\xff\xf0\x00\x7f\xff\xd0\x00\x7f\xff\xc0\x00\x3f\xff\xc0\x00\x3f\xff\xc0\x00\x1f\xff\x80\x00\x0f\xfe\x00\x00\x03\xec\x00\x00\x01\xc4\x00\x00\x01\x84\x00\x00\x01\x04\x00\x00\x01\x86\x00\x00"
        )

    def update(self, display, jump_info):
        image_render = framebuf.FrameBuffer(
            self.dino_image, self.width, self.height, framebuf.MONO_HLSB
        )
        image_render_right = framebuf.FrameBuffer(
            self.dino_right_leg_image, self.width, self.height, framebuf.MONO_HLSB
        )
        image_render_left = framebuf.FrameBuffer(
            self.dino_left_leg_image, self.width, self.height, framebuf.MONO_HLSB
        )

        if self.current_x != self.x:
            self.current_x = self.x

        if self.y == self.current_y and jump_info:
            self.current_y -= 4
            display.blit(image_render, self.current_x, self.current_y)
            self.state = 1
        elif self.state == 1:
            if self.current_y == 0:
                if self.top_slower_index == self.top_slower:
                    self.state = 2
                    self.top_slower = 0
                else:
                    self.top_slower += 1

                display.blit(image_render, self.current_x, self.current_y)
            else:
                if not (self.current_y < 6 and self.current_y > 0):
                    self.current_y -= 4
                else:
                    self.current_y -= 1
                display.blit(image_render, self.current_x, self.current_y)
        elif self.state == 2:
            if self.current_y == self.y:
                self.state = 0
                display.blit(image_render, self.current_x, self.current_y)
            else:
                if self.current_y > 33 and self.current_y <= 37:
                    self.current_y += 1
                else:
                    self.current_y += 2
                display.blit(image_render, self.current_x, self.current_y)
        else:
            if self.legs_counter <= (self.legs_counter_index / 2):
                self.legs_counter += 1
                display.blit(image_render_left, self.x, self.y)
            elif self.legs_counter > (self.legs_counter_index / 2):
                display.blit(image_render_right, self.x, self.y)
                self.legs_counter += 1
                if self.legs_counter_index == self.legs_counter + 1:
                    self.legs_counter = 0

    def game_logo(self, display):
        image_render_right = framebuf.FrameBuffer(
            self.dino_right_leg_image, self.width, self.height, framebuf.MONO_HLSB
        )
        image_render_left = framebuf.FrameBuffer(
            self.dino_left_leg_image, self.width, self.height, framebuf.MONO_HLSB
        )

        if self.legs_counter <= (self.legs_counter_index / 2):
            self.legs_counter += 1
            self.current_x += 1
            if self.current_x > self.max_screen_size:
                self.current_x = -self.width
            display.blit(image_render_left, self.current_x, self.current_y)
        elif self.legs_counter > (self.legs_counter_index / 2):
            self.current_x += 1
            if self.current_x > self.max_screen_size:
                self.current_x = -self.width
            display.blit(image_render_right, self.current_x, self.current_y)
            self.legs_counter += 1
            if self.legs_counter_index == self.legs_counter + 1:
                self.legs_counter = 0

    def game_over(self, display):
        image_render = framebuf.FrameBuffer(
            self.dino_image_dead, self.width, self.height, framebuf.MONO_HLSB
        )
        display.blit(
            image_render,
            int(((self.max_screen_size - 1) / 2) - (self.width / 2)),
            self.y,
        )

    def reset(self):
        self.current_x = self.x
        self.current_y = self.y
