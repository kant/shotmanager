# GPLv3 License
#
# Copyright (C) 2020 Ubisoft
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Utility functions for opengl overlay
"""

from collections import defaultdict
from statistics import mean

import gpu
import bgl, blf
import bpy
from gpu_extras.batch import batch_for_shader

#
# Blender windows system utils
#
def get_region_at_xy(context, x, y, area_type="VIEW_3D"):
    """
    Does not support quadview right now

    :param context:
    :param x:
    :param y:
    :return: the region and the area containing this region
    """
    for area in context.screen.areas:
        if area.type != area_type:
            continue
        # is_quadview = len ( area.spaces.active.region_quadviews ) == 0
        i = -1
        for region in area.regions:
            if region.type == "WINDOW":
                i += 1
                if region.x <= x < region.width + region.x and region.y <= y < region.height + region.y:

                    return region, area

    return None, None


#
# Geometry utils functions
#
class Square:
    UNIFORM_SHADER_2D = gpu.shader.from_builtin("2D_UNIFORM_COLOR")

    def __init__(self, x, y, sx, sy, color=(1.0, 1.0, 1.0, 1.0)):
        self._x = x
        self._y = y
        self._sx = sx
        self._sy = sy
        self._color = color

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def sx(self):
        return self._sx

    @sx.setter
    def sx(self, value):
        self._sx = value

    @property
    def sy(self):
        return self._sy

    @sy.setter
    def sy(self, value):
        self.sy = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    def copy(self):
        return Square(self.x, self.y, self.sx, self.sy, self.color)

    def draw(self):
        vertices = (
            (-self._sx + self._x, self._sy + self._y),
            (self._sx + self._x, self._sy + self._y),
            (-self._sx + self._x, -self._sy + self._y),
            (self._sx + self._x, -self._sy + self._y),
        )
        # vertices += [ pos_2d.x, pos_2d.y ]
        indices = ((0, 1, 2), (2, 1, 3))

        batch = batch_for_shader(self.UNIFORM_SHADER_2D, "TRIS", {"pos": vertices}, indices=indices)

        self.UNIFORM_SHADER_2D.bind()
        self.UNIFORM_SHADER_2D.uniform_float("color", self._color)
        batch.draw(self.UNIFORM_SHADER_2D)

    def bbox(self):
        return (-self._sx + self._x, -self.sy + self._y), (self._sx + self._x, self._sy + self._y)

