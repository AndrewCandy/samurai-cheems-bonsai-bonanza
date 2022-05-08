"""
This module allows us to test some important aspects of our view file
"""

import pytest
import pygame
from pymunk import Vec2d
from view import (center_offset, vec_to_tuple, rescale)

pygame.init()

# Test cases for offset
offset_cases = [

    # Test offset for square object
    (pygame.Surface((100, 100)), Vec2d(100, 100), Vec2d(50, 50)),

    # Test offset into negative coordinates
    (pygame.Surface((100, 100)), Vec2d(25, 25), Vec2d(-25, -25)),

    # Test non-square object
    (pygame.Surface((20, 40)), Vec2d(100, 100), Vec2d(90, 80)),
]

# Test cases for vector to tuple
tuple_cases = [

    # Testing no rounding
    (Vec2d(2, 3), (2, 3)),

    # Testing round down
    (Vec2d(2.0333, 3.023200), (2, 3)),

    # Testing round up
    (Vec2d(2.909, 3.909), (3, 4)),
]

# Test cases for rescaling
rescale_cases = [

    # Test resize to same size
    (pygame.Surface((10, 10)), (10, 10)),

    # Test resize to smaller size
    (pygame.Surface((10, 10)), (5, 5)),

    # Test resize to larger size
    (pygame.Surface((10, 10)), (20, 20)),

    # Test resize to different heights and widths
    (pygame.Surface((10, 10)), (10, 30)),
]


@pytest.mark.parametrize("image, position, offset", offset_cases)
def test_center_offset(image, position, offset):
    """
    This is the basic testing structure for the center offset function
    """

    output = center_offset(image, position)

    output_tuple = (output.x, output.y)

    assert output_tuple == offset


@pytest.mark.parametrize("vec, test_tuple", tuple_cases)
def test_vec_to_tuple(vec, test_tuple):
    """
    This is the basic testing structure for the vec to tuple function
    """

    assert vec_to_tuple(vec) == test_tuple


@pytest.mark.parametrize("image, dimensions", rescale_cases)
def test_rescale(image, dimensions):
    """
    This is the basic testing structure for the rescale function
    """

    objects = rescale(image, dimensions)

    output = (objects.get_width(), objects.get_height())

    assert output == dimensions
