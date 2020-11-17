import os

import arcade

from running_dinosaur_esgi.game_objects import *

from running_dinosaur_esgi.global_variables import *


class Environment:
    def __init__(self):
        self.states = {}
        self.height = SCREEN_HEIGHT
        self.width = SCREEN_WIDTH
        self.starting_point = (SCREEN_WIDTH / 6, SCREEN_HEIGHT / 2)
        self.setup()

    def updateStates(self, obstacles):
        self.states = {}
        for sprite in obstacles:
            self.states[(sprite.center_x, sprite.center_y)] = '#'

    def drawEnvironment(self):
        print('*****************************')
        for obstacle in self.states:
            print('state =', obstacle);
        print('*****************************')

    def setup(self):
        self.gameObject = []
        self.gameObjectFactory = GameObjectFactory()
        self.totalScrool = 0

    def apply(self, state, action):
        # replace 50 et 20 with the value of jumps and down
        if action == UP:
            new_state = (state[0], state[1] + 50)
        elif action == DOWN:
            new_state = (state[0], state[1] - 20)

        if new_state in self.states:
            # calculer la récompense
            #faire un interval
            if self.states[new_state] in ['#']:
                reward = REWARD_STUCK
            else:
                reward = REWARD_DEFAULT

        return new_state, reward

    def update(self, scroolSpeed):
        self.scrool(scroolSpeed)
        appendNewObstacle = random_case()
        if appendNewObstacle == 7:
            self.__spawn_service()

    def clean(self):
        if (len(self.gameObject) > 0):
            if self.gameObject[0].x - self.gameObject[0].scrool < 0:
                del self.gameObject[0]

    def scrool(self, scroolSpeed):
        self.totalScrool += scroolSpeed
        for i in self.gameObject:
            i.addScrool(scroolSpeed)

    def __spawn_service(self):
        last_spawn = 0
        if len(self.gameObject) != 0:
            last_spawn = min(self.gameObject, key=attrgetter('scrool')).scrool

        if (len(self.gameObject) == 0 or last_spawn > 215):
            self.spawn()

    def spawn(self):
        self.gameObject.append(self.gameObjectFactory.createRambdomObject())


class Agent:
    def __init__(self, environment):
        self.environment = environment
        self.policy = Policy(environment.states.keys(), ACTIONS)
        #to-do update the policy with the keys
        self.reset()

    def updatePolicyWithNewStates(self, newStates):
        self.policy.updateEnvironmentStates(newStates)

    def reset(self):
        self.state = self.environment.starting_point
        self.previous_state = self.state
        self.score = 0

    def best_action(self):
        return self.policy.best_action(self.state)

    def do(self, action):
        self.previous_state = self.state
        self.state, self.reward = self.environment.apply(self.state, action)
        self.score += self.reward
        self.last_action = action

    def update_policy(self):
        self.policy.update(agent.previous_state, agent.state, self.last_action, self.reward)

class Policy:  # Q-table  (self, states de l'environnement, actions <<up, down>>)
    def __init__(self, states, actions,
                 learning_rate=DEFAULT_LEARNING_RATE,
                 discount_factor=DEFAULT_DISCOUNT_FACTOR):
        self.actions = actions
        self.table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        print('states =', states)
        for s in states:
            self.table[s] = {}
            for a in actions:
                self.table[s][a] = 0

    def updateEnvironmentStates(self, newStates):
        for s in newStates:
            self.table[s] = {}
            for a in self.actions:
                self.table[s][a] = 0

    def __repr__(self):
        res = ''
        for state in self.table:
            res += f'{state}\t{self.table[state]}\n'
        return res

    def best_action(self, state):
        action = None
        print('self.table =', self.table)
        print('state =', state)
        if bool(self.table): #check if table in not empty due to environment states update
            for a in self.table[state]:
                print('a =', a)
                if action is None or self.table[state][a] > self.table[state][action]:
                    action = a
        return action

    def update(self, previous_state, state, last_action, reward):
        # Q(st, at) = Q(st, at) + learning_rate * (reward + discount_factor * max(Q(state)) - Q(st, at))
        maxQ = max(self.table[state].values())
        self.table[previous_state][last_action] += self.learning_rate * \
                                                   (reward + self.discount_factor * maxQ - self.table[previous_state][
                                                       last_action])


def gameOver():
    print("Game Over")


class Game(arcade.Window):
    def __init__(self, agent):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.agent = agent
        self.background = arcade.load_texture("resources/background.png")
        self.dinosaur = arcade.Sprite("resources/dinosaur_frame3.png", DINO_SIZE)

    def setup(self):
        self.is_falling = False
        self.is_lay_down = False
        self.is_jumping = False
        self.dinosaur_currentFrame = 1
        self.nb_laying_down_frames = 0
        self.nb_transition_enviromment_frames = 0

        self.update_dinosaur_xy_on_start_point()

        self.prepare_obstacles()
        self.agent.environment.setup()

    def prepare_obstacles(self):
        self.obstacles = arcade.SpriteList()
        self.agent.environment.clean()  # delete gameObject with negative absis x
        for n in agent.environment.gameObject:
            sprite = arcade.Sprite(PREFIX_RESSOURCE + n.getCurrentSprite(), DINO_SIZE)
            sprite.center_x = n.x - n.scrool
            sprite.center_y = n.y
            self.obstacles.append(sprite)

        self.agent.environment.updateStates(self.obstacles)
        #self.agent.environment.drawEnvironment()

    def update_enviromment(self):
        self.agent.environment.update(15)
        self.prepare_obstacles()
        # if (len(arcade.check_for_collision_with_list(self.dinosaur, self.obstacles)) > 0):
        # self.gameOver()

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
        if key == arcade.key.DOWN:
            self.is_lay_down = True
        if self.is_jumping is False and key == arcade.key.SPACE:
            print('jumping')
            self.is_jumping = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.DOWN:
            self.is_lay_down = False

    def fall(self):
        self.dinosaur.center_y -= GRAVITY_CONSTANT

    def jump(self):
        self.dinosaur.center_y += GRAVITY_CONSTANT

    def updateAndRenderGame(self, _delta_time):
        self.nb_transition_enviromment_frames += 1
        if self.nb_transition_enviromment_frames > TRANSITION_FRAMES:
            self.nb_transition_enviromment_frames = 0
            self.update_enviromment()

        self.gravitySimulator()

        if self.is_falling is False and self.is_jumping is False:
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

    def gravitySimulator(self):
        if self.is_jumping:
            if self.dinosaur.center_y <= SCREEN_HEIGHT / 2 + SEEKED_JUMP_HEIGHT:
                self.jump()
            else:
                self.is_jumping = False
                self.is_falling = True
        if self.is_falling:
            self.is_jumping = False
            if self.dinosaur.center_y > self.agent.state[1] + 30:
                self.fall()
            else:
                self.is_jumping = False
                self.is_falling = False
                self.update_dinosaur_xy_on_start_point()

    def on_update(self, delta_time):
        self.agent.updatePolicyWithNewStates(self.agent.environment.states.keys())
        action = self.agent.best_action()
        #self.agent.do(action)
        #self.agent.update_policy()
        #self.update_player_xy()


if __name__ == "__main__":
    # Initialiser l'agent
    environment = Environment()
    agent = Agent(environment)
    window = Game(agent)
    window.setup()
    arcade.schedule(window.updateAndRenderGame, 1 / 50)
    arcade.run()
