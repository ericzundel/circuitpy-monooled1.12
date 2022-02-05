# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
Author: Mark Roberts (mdroberts1243) from Adafruit code
This test will initialize the display using displayio and draw a solid white
background, a smaller black rectangle, miscellaneous stuff and some white text.

Updated by Eric Ayers to put into a class and set the correct board address
and display offset for the Mono OLED 1.12in display http://adafru.it/5297
"""


import board
import displayio
import terminalio
import busio

# can try import bitmap_label below for alternative
from adafruit_display_text import label
import adafruit_displayio_sh1107

DISPLAY_I2C_ADDRESS = 0x3D

WIDTH = 128
HEIGHT = 128
BORDER = 2

class screen:
    """
    A series of test screens
    """

    def __init__(self,  **kwargs):
        displayio.release_displays()
        # oled_reset = board.D9
        # Use for default I2C
        i2c = board.I2C()
        # Attempt to increase frequency
        #i2c = busio.I2C(scl=board.SCL, sda=board.SDA, frequency=400000)
        display_bus = displayio.I2CDisplay(i2c, device_address=DISPLAY_I2C_ADDRESS)
        self.display = adafruit_displayio_sh1107.SH1107(
            display_bus, width=WIDTH, height=HEIGHT, rotation=0,
            display_offset=adafruit_displayio_sh1107.DISPLAY_OFFSET_PIMORONI_MONO_OLED_PIM374
        )

        self.color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
        self.color_palette = displayio.Palette(1)
        self.color_palette[0] = 0xFFFFFF  # White

    def splash(self):
        # Make the display context
        splash = displayio.Group()
        #self.display.show(splash)

        bg_sprite = displayio.TileGrid(self.color_bitmap, pixel_shader=self.color_palette, x=0, y=0)
        splash.append(bg_sprite)

        # Draw a smaller inner rectangle in black
        inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = 0x000000  # Black
        inner_sprite = displayio.TileGrid(
            inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
        )
        splash.append(inner_sprite)

        # Draw some white squares
        sm_bitmap = displayio.Bitmap(8, 8, 1)
        sm_square = displayio.TileGrid(sm_bitmap, pixel_shader=self.color_palette, x=58, y=17)
        splash.append(sm_square)

        med_bitmap = displayio.Bitmap(16, 16, 1)
        med_square = displayio.TileGrid(med_bitmap, pixel_shader=self.color_palette, x=71, y=15)
        splash.append(med_square)

        lrg_bitmap = displayio.Bitmap(32, 32, 1)
        lrg_square = displayio.TileGrid(lrg_bitmap, pixel_shader=self.color_palette, x=91, y=28)
        splash.append(lrg_square)

        # Draw some label text
        text1 = "0123456789ABCDEF123456789AB"  # overly long to see where it clips
        text_area = label.Label(terminalio.FONT, text=text1, color=0xFFFFFF, x=8, y=8)
        splash.append(text_area)
        text2 = "SH1107"
        text_area2 = label.Label(
            terminalio.FONT, text=text2, scale=2, color=0xFFFFFF, x=9, y=44
        )
        splash.append(text_area2)
        self.display.show(splash)

    def origin(self):
        screen = displayio.Group()
        self.display.show(screen)

        tiny_bitmap = displayio.Bitmap(2, 2, 1)
        tiny_square = displayio.TileGrid(tiny_bitmap, pixel_shader=self.color_palette, x=0, y=0)
        screen.append(tiny_square)

    def triangle(self):
        screen = displayio.Group()
        self.display.show(screen)

        logo_bitmap = displayio.Bitmap(8, 8, 1)
        #logo_shape = displayio.Shape(8, 8, [0x01, 0x03, 0x07, 0x15, 0x31, 0x63, 0x127, 0x255])
        for i in range(0,8):
            for j in range(i,8):
                logo_bitmap[i,j] = 1;
        logo = displayio.TileGrid(logo_bitmap, pixel_shader=self.color_palette, x=0, y=0)
        screen.append(logo)

    def drew_logo(self):
        screen = displayio.Group()
        self.display.show(screen)

        with open("drew_logo.bmp", "rb") as bitmap_file:
            bitmap = displayio.OnDiskBitmap(bitmap_file)
            logo = displayio.TileGrid(bitmap, pixel_shader=self.color_palette, x=0, y=0)
            screen.append(logo)
