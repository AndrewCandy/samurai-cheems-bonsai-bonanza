"""
Creates the class SpriteSheet to create pygame surfaces
from image files.
"""

import pygame


class SpriteSheet:
    """
    Loads sprites from image files to turn them into pygame surfaces.

    Attributes:
        self.sheet: A pygame surface loaded from an image file at filename.
    """

    def __init__(self, filename):
        """
        Creates an instance of the SpriteSheet class.

        Attributes:
            self.sheet: A pygame surface loaded from an image file at filename.
        """
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as error:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(error) from error

    def image_at(self, rectangle, colorkey = None):
        """
        loads an image from a specified rectangle of a sprite sheet.

        Args:
            rectangle: A tuple of form (x, y, x_offset, y_offset).
            colorkey: An Int representing a colorkey. -1 is used for PNG's to
                      preserve transparency.

        Returns:
            A pygame surface containing the portion of the sprite sheet
            specified.
        """
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.fill(pygame.Color("Red"))
        image.blit(self.sheet, (0,0), rect)

        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey = None):
        """
        loads a list of images from a list of rectangles on a sprite sheet.

        Args:
            rectangles: A list of tuples of form (x, y, x_offset, y_offset).
            colorkey: An Int representing a colorkey. -1 is used for PNG's to
                      preserve transparency.

        Returns:
            A list of pygame surfaces containing the specified sections of the
            sprite sheet.
        """
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey = None):
        """
        loads a list of horizontally adjacent images from a sprite sheet.

        Args:
            rect: A Tuple of form (x, y, x_offset, y_offset).
            image_count: An int representing the total number of images in the
                         row.
            colorkey: An Int representing a colorkey. -1 is used for PNG's to
                      preserve transparency.

        Returns:
            A list of pygame surfaces containing the specified sections of the
            sprite sheet.
        """
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])\
             for x in range(image_count)]
        return self.images_at(tups, colorkey)
