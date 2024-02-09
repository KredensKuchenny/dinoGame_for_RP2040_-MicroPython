import framebuf
import random


class Cloud:
    def __init__(self, cloud_width, cloud_height, clouds_width, clouds_height, x, y):
        self.cloud_width = cloud_width
        self.cloud_height = cloud_height
        self.clouds_width = clouds_width
        self.clouds_height = clouds_height
        self.x = x
        self.y = y
        self.current_x = self.x
        self.current_y = self.y
        self.counter = 1
        self.image_type = 0
        self.cloud = bytearray(
            b"\x00\x00\x70\x00\x00\x02\x04\x00\x00\x0c\x00\x00\x00\x00\x01\xe0\x00\x30\x00\x10\x00\x40\x00\x04\x08\x00\x00\x02\x10\x00\x00\x00\x81\xff\xff\xff"
        )
        self.clouds = bytearray(
            b"\x00\x00\x00\x00\x38\x00\x00\x00\x00\x02\x04\x00\x00\x00\x70\x0c\x02\x00\x00\x04\x0c\x08\x02\xe0\x00\x08\x04\x38\x00\x10\x00\x00\x07\xe0\x00\x04\x00\x30\x08\x00\x00\x02\x00\xc0\x08\x08\x00\x00\x08\x00\x40\xff\xff\xff\x10\x00\x00\x00\x00\x00\x81\xff\xff\xfe\x00\x00"
        )

    def update(self, display):
        image_render = framebuf.FrameBuffer(
            self.cloud, self.cloud_width, self.cloud_height, framebuf.MONO_HLSB
        )
        images_render = framebuf.FrameBuffer(
            self.clouds, self.clouds_width, self.clouds_height, framebuf.MONO_HLSB
        )

        if self.current_x == self.x:
            self.image_type = random.randint(0, 1)

        if self.image_type:
            self.current_x -= 1
            display.blit(image_render, self.current_x, self.current_y)
            if self.current_x == -self.cloud_width:
                self.current_x = self.x
                self.counter += 1
        else:
            self.current_x -= 1
            display.blit(images_render, self.current_x, self.current_y)
            if self.current_x == -self.clouds_width:
                self.current_x = self.x
                self.counter += 1
