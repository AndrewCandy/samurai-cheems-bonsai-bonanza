"""
Creates the main game file for Samurai Cheems: Bonsai Bonanza
"""

# Library imports
import pygame

from board import Board
from view import DefaultView
from controller import MouseController
import sound

# Initialize sound system
music = sound.initialize_mixer()
sound.loop_music()


def main():
    """
    Sets up the model, view, and controller and uses them to run each level
    of Samurai Cheems: Bonsai Bonanza
    """
    # Sets up the Board, the view, and the controller
    game = Board()
    game_view = DefaultView(game)
    game_controller = MouseController(game)

    # Draws the walls and background of the game
    game.draw_background()

    # Uses the number of levels and number of stages per level to
    # Iterate through each stage of the game
    num_levels = 1
    num_stages = 3

    # Iterates for each level and stage
    for level in range(num_levels):
        for stage in range(num_stages):
            # Draws the upcoming level
            game.draw_level(level+1, stage+1)
            # Runs the game for that level
            run(game, game_view, game_controller, stage)

    print("You Win!")


def run(game, game_view, game_controller, stage):
    """
    Runs through the main gameplay loop for each level
    """
    # Ends this level if the game ends or if the game is closed or the score
    # is high enough
    while game_controller.running and stage in game.get_scores():
        # Progress time forward
        for x in range(game.physics_steps_per_frame):
            game._space.step(game.dt)

        # Checks for keyboard events
        game_controller.process_events()
        # Check if the ball is in the pot
        game.check_if_scored()
        # Redraws the background
        game_view.clear_screen()
        # Draws the active screen objects
        game_view.draw_objects()

        # Delay fixed time between frames
        game._clock.tick(50)

        #Set window title
        pygame.display.set_caption(f"Your score is {game.get_scores()}!")


if __name__ == "__main__":
    main()
