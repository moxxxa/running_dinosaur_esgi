import os
import time
from abc import abstractmethod

import arcade
import numpy

from GameObject import *

from enum import Enum


def random_case():
    return numpy.random.choice(numpy.arange(1, 10), p=[0.6, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05])

def random_distance():
    distanceProb =  numpy.random.choice(numpy.arange(1, 8), p=[0.03, 0.07, 0.1, 0.15, 0.2, 0.2, 0.25])
    if distanceProb == 1:
        return 30
    elif distanceProb == 2:
        return 70
    elif distanceProb == 3:
        return 90
    elif distanceProb == 4:
        return 110
    elif distanceProb == 5:
        return 135
    elif distanceProb == 6:
        return 170
    elif distanceProb == 7:
        return 200

class Agent:
    def __init__(self, environment):
        self.environment = environment
        # self.policy = Policy(environment.states.keys(), ACTIONS)
        self.reset()

    def reset(self):
        self.state = environment.starting_point
        self.previous_state = self.state
        self.score = 0


class Policy:  # Q-table  (self, states de l'environnement, actions <<up, down>>)
    def __init__(self, states, actions,
                 learning_rate=DEFAULT_LEARNING_RATE,
                 discount_factor=DEFAULT_DISCOUNT_FACTOR):
        print('policy init')

class Game(arcade.Window):
    def __init__(self, agent):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.agent = agent

    def setup(self):
        self.background = arcade.load_texture("resources/background.png")
        self.dinosaur = arcade.Sprite("resources/dinosaur_frame3.png", DINO_SIZE)
        self.obstacles = arcade.SpriteList()

        self.is_falling = False
        self.is_lay_down = False
        self.dinosaur_currentFrame = 1
        self.nb_laying_down_frames = 0
        self.nb_transition_frames = 0
        self.update_dinosaur_xy_on_start_point()
        self.testSprite = arcade.Sprite("resources/dinosaur_frame3.png", DINO_SIZE)
        self.testIsCreate = False

        self.prepare_obstacles()
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.dinosaur,
                                                             self.obstacles,
                                                             1)
        self.agent.environment.update(3)

    def prepare_obstacles(self):
        self.obstacles = arcade.SpriteList()

        for n in agent.environment.gameObject:

            sprite = arcade.Sprite(PREFIX_RESSOURCE + n.getCurrentSprite(), DINO_SIZE)
            sprite.center_x = n.x - n.scrool
            sprite.center_y = n.y
            self.obstacles.append(sprite)


    def update_enviromment(self):
        self.agent.environment.update(15)
        self.prepare_obstacles()
        self.physics_engine.update()
        self.dinosaur.change_x = 20
        if(len(arcade.check_for_collision_with_list(self.dinosaur, self.obstacles)) > 0):
            self.gameOver()

    def update_dinosaur_xy_on_start_point(self):
        self.dinosaur.center_x = self.agent.state[0] - 30
        self.dinosaur.center_y = self.agent.state[1] + 30

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        self.dinosaur.draw()
        arcade.draw_text(f"Score: {self.agent.score}", 10, 10, arcade.csscolor.BLACK, 20)
        self.obstacles.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.agent.reset()
            self.setup()
        if key == arcade.key.UP:
            self.dinosaur.change_y = 600
            if self.physics_engine.can_jump():
                self.dinosaur.change_y = PLAYER_JUMP_SPEED
        if key == arcade.key.DOWN:
            self.is_lay_down = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.DOWN:
            self.is_lay_down = False

    def fall(self):
        self.dinosaur.center_y -= GRAVITY_CONSTANT

    def updateAndRenderGame(self, _delta_time):
        self.nb_transition_frames += 1
        if self.nb_transition_frames > TRANSITION_FRAMES:
            self.nb_transition_frames = 0
            self.update_enviromment()
        if  self.is_falling is False:
            self.update_dinosaur_frame()

        self.agent.score += 1


    def update_dinosaur_frame(self):
        self.dinosaur_currentFrame += 1
        if self.dinosaur_currentFrame > 10:
            self.dinosaur_currentFrame = 1

        if self.dinosaur_currentFrame <= 5:
            if self.is_lay_down == True:
                self.dinosaur = arcade.Sprite("resources/dinosaur_frame4.png", DINO_SIZE)
            else:
                self.dinosaur = arcade.Sprite("resources/dinosaur_frame1.png", DINO_SIZE)
        elif self.dinosaur_currentFrame > 5:
            if self.is_lay_down == True:
                self.dinosaur = arcade.Sprite("resources/dinosaur_frame5.png", DINO_SIZE)
            else:
                self.dinosaur = arcade.Sprite("resources/dinosaur_frame2.png", DINO_SIZE)
        elif self.is_lay_down == True:
            self.dinosaur = arcade.Sprite("resources/dinosaur_frame4.png", DINO_SIZE)
        else:
            self.dinosaur = arcade.Sprite("resources/dinosaur_frame3.png", DINO_SIZE)

        self.update_dinosaur_xy_on_start_point()

    def gameOver(self):
        print("Game Over")

if __name__ == "__main__":
    # Initialiser l'agent
    environment = Environment()
    agent = Agent(environment)
    window = Game(agent)
    window.setup()
    arcade.schedule(window.updateAndRenderGame, 1 / 80)
    arcade.run()
