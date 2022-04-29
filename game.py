# Python imports
import random
from typing import List

# Library imports
import pygame

# pymunk imports
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
from board import Board

"""
Main program to set up and run a tic-tac-toe game.
"""
from levels import LevelLayout
from board import Board
from view import DefaultView
from controller import MouseController

def main():
    
    """
    The main loop of the game.
    :return: None
    """
    #Sets up the Board, the view, and the controllers
    level = LevelLayout(0,0)
    
    running = True
    # Main loop
    game = Board()
    game_view = DefaultView(game)
    game_controller = MouseController(game)

    game.draw_background()
    game.draw_level(1,1)
    while game_controller._running:
            # Progress time forward
            for x in range(game._physics_steps_per_frame):
                game._space.step(game._dt)

            game_controller._process_events()
            game.check_if_scored()
            game_view.clear_screen()
            game_view.draw_objects()
            pygame.display.flip()
            # Delay fixed time between frames
            game._clock.tick(50)
            pygame.display.set_caption(f"Your score is {game.score}!")

if __name__ == "__main__":
    main()