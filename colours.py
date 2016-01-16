"""
Copyright (C) 2014 Linus Heckemann

This file is part of Pirates.

Pirates is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Pirates is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Pirates.  If not, see <http://www.gnu.org/licenses/>.
"""
from pygame import Color
# Grid colours
square_colour_visible = Color(128, 128, 255)
square_colour_hidden = Color(64, 64, 96)
square_colour_visible_ship = Color(0, 0, 192)
background_colour = Color(0, 32, 64)

# Ship colours
default_colour = Color(128, 128, 128, 255)
destroyed_colour = Color(0, 0, 128, 255)
preplaced_colour = Color(128, 255, 128, 128)
prepicked_colour = Color(255, 255, 0, 128)
error_colour = Color(255, 0, 0, 128)
