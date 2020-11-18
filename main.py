import os

import arcade

from running_dinosaur_esgi.game_objects import *

from running_dinosaur_esgi.global_variables import *


GLOBAL_JUMP = False
GLOBAL_FALL = False
GLOBAL_LAYDOWN = False
GLOBAL_Y = -1
GLOBAL_COLISION = False

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
        global GLOBAL_JUMP
        global GLOBAL_LAYDOWN
        global GLOBAL_COLISION

        if action == UP and GLOBAL_JUMP == False and GLOBAL_FALL == False:
            GLOBAL_JUMP = True
        elif action == DOWN and GLOBAL_LAYDOWN == False and GLOBAL_FALL == False and GLOBAL_JUMP == False:
            GLOBAL_LAYDOWN = True
        elif action == WALK:
            print('Walking')

        if GLOBAL_COLISION:
                reward = REWARD_STUCK
        else:
            reward = REWARD_DEFAULT # make reward default equal to zero and take account only the global score

        GLOBAL_COLISION = False

        return (state[0], GLOBAL_Y), reward

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
        self.policy.updatePolicyWithNewStates(newStates)

    def updatePolicyWithDinoPosition(self, dinoState):
        self.policy.updatePolicyWithDinoPosition(dinoState)

    def reset(self):
        self.state = self.environment.starting_point
        self.previous_state = self.state
        self.score = 0

    def best_action(self):
        return self.policy.best_action(self.state)

    def do(self, action):
        #print('action =', action)
        self.previous_state = self.state
        self.state, self.reward = self.environment.apply(self.state, action)
        print('after the do, state =', self.state, '   self.reward =', self.reward);
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
        for s in states:
            self.table[s] = {}
            for a in actions:
                self.table[s][a] = 0

    def updatePolicyWithNewStates(self, newStates):
        #print('newStates =', newStates);
        #print('self.actions =', self.actions);
        for s in newStates:#les nouveaux obstacle
            if not s in self.table: # c'est-a-dire self.table[s] est vide
                self.table[s] = {}
                for a in self.actions:
                    self.table[s][a] = 0
        #print('updatePolicy, self.table =', self.table)

    def updatePolicyWithDinoPosition(self, dinoState):
        if not dinoState in self.table: # c'est-a-dire self.table[dinoState] est vide
            self.table[dinoState] = {}
            for a in self.actions:
                self.table[dinoState][a] = 0

    def __repr__(self):
        res = ''
        for state in self.table:
            res += f'{state}\t{self.table[state]}\n'
        return res

    def best_action(self, state):#state = position de dino (x,y)
        action = None
        #print('self.table =', self.table)
        #print('state =', state)
        if bool(self.table): #check if table in not empty due to environment states update
            for a in self.table[state]:
                if action is None or self.table[state][a] > self.table[state][action]:
                    action = a
        return action

    def update(self, previous_state, state, last_action, reward):
        # Q(st, at) = Q(st, at) + learning_rate * (reward + discount_factor * max(Q(state)) - Q(st, at))
        if state in self.table:
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
        global GLOBAL_JUMP
        global GLOBAL_LAYDOWN
        global GLOBAL_FALL
        global GLOBAL_COLISION
        GLOBAL_COLISION = False
        GLOBAL_JUMP = False
        GLOBAL_FALL = False
        GLOBAL_LAYDOWN = False
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
        global GLOBAL_COLISION
        self.agent.environment.update(15)
        self.prepare_obstacles()
        if (len(arcade.check_for_collision_with_list(self.dinosaur, self.obstacles)) > 0):
            GLOBAL_COLISION = True

    def update_dinosaur_xy_on_start_point(self):
        self.dinosaur.center_x = self.agent.environment.starting_point[0] - 30
        self.dinosaur.center_y = self.agent.environment.starting_point[1] + 30

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        self.dinosaur.draw()
        arcade.draw_text(f"Score: {self.agent.score}", 10, 10, arcade.csscolor.BLACK, 20)
        self.obstacles.draw()

    def on_key_press(self, key, modifiers):
        global GLOBAL_JUMP
        global GLOBAL_LAYDOWN
        if key == arcade.key.R:
            self.agent.reset()
            self.setup()
        if key == arcade.key.UP:
            self.dinosaur.change_y = 600
        if key == arcade.key.DOWN:
            GLOBAL_LAYDOWN = True
        if GLOBAL_JUMP == False and key == arcade.key.SPACE:
            print('jumping')
            GLOBAL_JUMP = True

    def on_key_release(self, key, modifiers):
        global GLOBAL_LAYDOWN
        if key == arcade.key.DOWN:
            GLOBAL_LAYDOWN = False

    def fall(self):
        self.dinosaur.center_y -= GRAVITY_CONSTANT

    def jump(self):
        self.dinosaur.center_y += GRAVITY_CONSTANT

    def updateAndRenderGame(self, _delta_time):
        global GLOBAL_LAYDOWN
        self.nb_transition_enviromment_frames += 1
        if self.nb_transition_enviromment_frames > TRANSITION_FRAMES:
            self.nb_transition_enviromment_frames = 0
            self.update_enviromment()

        self.gravitySimulator()


        if GLOBAL_FALL == False and GLOBAL_JUMP == False:
            self.update_dinosaur_frame()

        #self.agent.score += 1

    def update_dinosaur_frame(self):
        self.dinosaur_currentFrame += 1
        if self.dinosaur_currentFrame > 10:
            self.dinosaur_currentFrame = 1

        if self.dinosaur_currentFrame <= 5:
            if GLOBAL_LAYDOWN == True:
                self.dinosaur = arcade.Sprite("resources/dinosaur_frame4.png", DINO_SIZE)
            else:
                self.dinosaur = arcade.Sprite("resources/dinosaur_frame1.png", DINO_SIZE)
        elif self.dinosaur_currentFrame > 5:
            if GLOBAL_LAYDOWN == True:
                self.dinosaur = arcade.Sprite("resources/dinosaur_frame5.png", DINO_SIZE)
            else:
                self.dinosaur = arcade.Sprite("resources/dinosaur_frame2.png", DINO_SIZE)
        elif GLOBAL_LAYDOWN == True:
            self.dinosaur = arcade.Sprite("resources/dinosaur_frame4.png", DINO_SIZE)
        else:
            self.dinosaur = arcade.Sprite("resources/dinosaur_frame3.png", DINO_SIZE)

        self.update_dinosaur_xy_on_start_point()

    def gravitySimulator(self):
        global GLOBAL_JUMP
        global GLOBAL_LAYDOWN
        global GLOBAL_FALL
        if GLOBAL_JUMP:
            if self.dinosaur.center_y <= SCREEN_HEIGHT / 2 + SEEKED_JUMP_HEIGHT:
                self.jump()
            else:
                GLOBAL_FALL = True


        if GLOBAL_FALL:
            GLOBAL_JUMP = False
            if self.dinosaur.center_y > self.agent.environment.starting_point[1] + 30:
                self.fall()
            else:
                GLOBAL_FALL = False
                self.update_dinosaur_xy_on_start_point()

    def on_update(self, delta_time):
        global GLOBAL_Y
        GLOBAL_Y = self.dinosaur.center_y
        self.updateAndRenderGame(delta_time)
        self.agent.updatePolicyWithDinoPosition(self.agent.state)
        self.agent.updatePolicyWithNewStates(self.agent.environment.states.keys())
        action = self.agent.best_action()
        self.agent.do(action)
        self.agent.update_policy()


if __name__ == "__main__":
    # Initialiser l'agent
    environment = Environment()
    agent = Agent(environment)
    window = Game(agent)
    window.setup()
    #arcade.schedule(window.updateAndRenderGame, 1 / 50)
    arcade.run()
