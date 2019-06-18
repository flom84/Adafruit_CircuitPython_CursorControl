# The MIT License (MIT)
#
# Copyright (c) 2019 Brent Rubell for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_cursor`
================================================================================

Simulated mouse cursor for display interaction


* Author(s): Brent Rubell

Implementation Notes
--------------------

**Hardware:**

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

* Adafruit's ImageLoad Library: https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad/
"""
from micropython import const
import adafruit_imageload
import displayio
import board

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Cursor.git"

class Cursor:
    """Mouse cursor-like interaction for CircuitPython.

    :param displayio.Display: CircuitPython display object.
    """
    def __init__(self, display=None, cursor_speed = 1, cursor=None):
        self._display = display
        self._display_width = display.width
        self._display_height = display.height
        self._speed = cursor_speed
        if cursor:
            self.load_custom_cursor(cursor)
        self.x = int(self._display_width/2)
        self.y = int(self._display_height/2)

    @property
    def speed(self):
        """Returns the cursor's speed."""
        return self._speed
    
    @speed.setter
    def speed(self, speed):
        """Sets the speed of the cursor.
        :param int speed: Cursor movement speed.
        """
        self._speed = speed

    @property
    def x(self):
        """Returns the cursor's x-coordinate."""
        return self._cursor_grp.x

    @x.setter
    def x(self, x_val):
        """Sets the x-value of the cursor.
        :param int x_val: x position, in pixels.
        """
        if (self._cursor_grp.x - self._speed < 0):
            self._cursor_grp.x = self._cursor_grp.x + 1
        elif self._cursor_grp.x + self._speed > self._display_width - 45:
            self._cursor_grp.x = self._cursor_grp.x - 1
        else:
            self._cursor_grp.x = x_val

    @property
    def y(self):
        """Returns the cursor's y-coordinate."""
        return self._cursor_grp.y

    @y.setter
    def y(self, y_val):
        """Sets the y-value of the cursor.
        :param int y_val: y position, in pixels.
        """
        if (self._cursor_grp.y - self._speed < 0):
            self._cursor_grp.y = self._cursor_grp.y + 1
        elif self._cursor_grp.y + self._speed > self._display_height - 45:
            self._cursor_grp.y = self._cursor_grp.y - 1
        else:
            self._cursor_grp.y = y_val        


    def load_custom_cursor(self, cursor_info):
        """ Loads and creates a custom cursor image from a defined spritesheet.
        """
        self._sprite_sheet, self._palette = adafruit_imageload.load(cursor_info['cursor_path'],
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)
        self._sprite = displayio.TileGrid(self._sprite_sheet, pixel_shader=self._palette,
                                    width = cursor_info['cursor_width'],
                                    height = cursor_info['cursor_height'],
                                    tile_width = cursor_info['cursor_tile_width'],
                                    tile_height = cursor_info['cursor_tile_height'])
        self._cursor_grp = displayio.Group(max_size = 1, scale=cursor_info['cursor_scale'])
        self._cursor_grp.append(self._sprite)
        self._display.show(self._cursor_grp)
