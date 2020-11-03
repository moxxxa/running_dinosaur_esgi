import os
import time

import arcade
import numpy

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Dinosaur runner"
UP, DOWN = 'U', 'D'
ACTIONS = [UP, DOWN]

REWARD_STUCK = -6
REWARD_DEFAULT = 1
DEFAULT_LEARNING_RATE = 1
DEFAULT_DISCOUNT_FACTOR = 0.5
LINE_OBJECT_LENGTH = 10
GRAVITY_CONSTANT = 10
JUMP_HEIGHT_SEEKED = 80
TRANSITION_FRAMES = 2

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

class Environment:
    def __init__(self):
        self.states = {}
        self.height = SCREEN_HEIGHT
        self.width = SCREEN_WIDTH
        self.starting_point = (SCREEN_WIDTH / 6, SCREEN_HEIGHT / 2)
        for i in range(LINE_OBJECT_LENGTH):
            case = random_case()
            if (case == 9 or case == 8) and (i != 0 and self.states[i - 1] != '#'):
                self.states[i] = '#'
            else:
                self.states[i] = '.'

            print(self.states)
    def apply(self, state, action):
        if action == UP:
            new_state = (state[0] - 1, state[1])
        elif action == DOWN:
            new_state = (state[0] + 1, state[1])


        if new_state in self.states:
            # calculer la récompense
            if self.states[new_state] in ['#']:
                reward = REWARD_STUCK
            else:
                reward = REWARD_DEFAULT

        return new_state, reward

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
        self.dinosaur = arcade.Sprite("resources/dinosaur_frame1.png", 0.5)
        self.is_jumping = False
        self.is_falling = False
        self.is_lay_down = False
        self.dinosaur_currentFrame = 1
        self.nb_laying_down_frames = 0
        self.nb_transition_frames = 0
        self.update_dinosaur_xy_on_start_point()
        self.prepare_obstacles()

    def prepare_obstacles(self):
        self.obstacles = arcade.SpriteList()
        for state in agent.environment.states:
            if agent.environment.states[state] == '#':
                sprite = arcade.Sprite("resources/obstacle.png", 0.5)
                sprite.center_x = (state + 1) * 100
                sprite.center_y = self.agent.state[1]
                self.obstacles.append(sprite)

    def update_enviromment(self):
        for i in range (1, LINE_OBJECT_LENGTH - 1):
            agent.environment.states[i - 1] = agent.environment.states[i]
        case = random_case()
        if (case == 9) and (agent.environment.states[i - 1] != '#'):
            agent.environment.states[i] = '#'
        else:
            agent.environment.states[i] = '.'
        self.prepare_obstacles()

    def update_dinosaur_xy_on_start_point(self):
        self.dinosaur.center_x = self.agent.state[0] - 15
        self.dinosaur.center_y = self.agent.state[1] + 15

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
        if key == arcade.key.SPACE and self.is_jumping is False:
            self.is_jumping = True
        if key == arcade.key.DOWN:
            self.is_lay_down = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.DOWN:
            self.is_lay_down = False

    def jump(self):
        self.dinosaur.center_y += GRAVITY_CONSTANT

    def fall(self):
        self.dinosaur.center_y -= GRAVITY_CONSTANT

    def updateAndRenderGame(self, _delta_time):
        self.nb_transition_frames += 1
        if self.nb_transition_frames > TRANSITION_FRAMES:
            self.nb_transition_frames = 0
            self.update_enviromment()

        self.gravitySimulator()
        if self.is_jumping is False and self.is_falling is False:
            self.update_dinosaur_frame()
        self.agent.score += 1

    def update_dinosaur_frame(self):
        self.dinosaur_currentFrame += 1

        if self.dinosaur_currentFrame > 3:
            self.dinosaur_currentFrame = 1

        if self.dinosaur_currentFrame == 1:
            if self.is_lay_down == True:
                self.dinosaur = arcade.Sprite("resources/dinosaur_frame4.png", 0.5)
            else:
                self.dinosaur = arcade.Sprite("resources/dinosaur_frame1.png", 0.5)
        elif self.dinosaur_currentFrame == 2:
            if self.is_lay_down == True:
                self.dinosaur = arcade.Sprite("resources/dinosaur_frame5.png", 0.5)
            else:
                self.dinosaur = arcade.Sprite("resources/dinosaur_frame2.png", 0.5)
        elif self.is_lay_down == True:
            self.dinosaur = arcade.Sprite("resources/dinosaur_frame4.png", 0.5)
        else:
            self.dinosaur = arcade.Sprite("resources/dinosaur_frame3.png", 0.5)
        self.update_dinosaur_xy_on_start_point()

    def gravitySimulator(self):
        if self.is_jumping:
            if self.dinosaur.center_y <= SCREEN_HEIGHT / 2 + JUMP_HEIGHT_SEEKED:
                self.jump()
            else:
                self.is_jumping = False
                self.is_falling = True
        elif self.is_falling:
            if self.dinosaur.center_y > self.agent.state[1] + 15:
                self.fall()
            else:
                self.is_jumping = False
                self.is_falling = False
                self.update_dinosaur_xy_on_start_point()


if __name__ == "__main__":

    # Initialiser l'agent
    environment = Environment()
    agent = Agent(environment)
    window = Game(agent)
    window.setup()
    arcade.schedule(window.updateAndRenderGame, 1 / 20)
    arcade.run()