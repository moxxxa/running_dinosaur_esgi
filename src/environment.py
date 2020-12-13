import arcade
import arcade
from src.global_variables import *
from src.game_objects import *

class Environment:
    def __init__(self):
        self.reset()

    def setup(self, agent):
        self.agent = agent
        self.physique_engine = arcade.PhysicsEnginePlatformer(self.agent,
                                                             self.ground_list,
                                                             GRAVITY)

    def update_collision(self):
        col_y =  self.enemy_list.colYWithAgent(self.agent)
        col_x =  self.enemy_list.colXWithAgent(self.agent)

        check_for_collision_with_list = len(arcade.check_for_collision_with_list(self.agent, self.enemy_list)) > 0

        if check_for_collision_with_list and col_x and col_y:
            self.collision = True

        if check_for_collision_with_list and col_x and not col_y:
            self.agent_is_below_enemy = True

        return col_x, col_y, check_for_collision_with_list


    def update(self):
        self.ground_list.scrool()
        self.ground_list.pop(1280)
        self.enemy_list.scrool()
        self.enemy_list.pop(2560)
        self.update_collision()
        self.total_scrool += SCROOL_SPEED

    def apply(self, action):
        if action == UP and self.physique_engine.can_jump():
            self.last_jump = self.agent.get_state()
            reward = REWARD_UP
            self.agent.change_y = PLAYER_JUMP_SPEED
            self.agent.walk()

        elif action == DOWN and self.physique_engine.can_jump():
            reward = REWARD_DOWN
            self.agent.down()
        else:
            reward = REWARD_DEFAULT
            self.agent.walk()

        if self.enemy_list.delete:
            reward += 200
            self.enemy_list.delete = False

        if self.collision:
            reward = REWARD_STUCK

        if not self.collision and self.agent_is_below_enemy:
            reward = REWARD_BELOW_ENEMY
            self.agent_is_below_enemy = False
            print("is below")

        return reward

    def reset(self):
        self.factory = Game_object_factory()
        self.ground_list = self.factory.init_grounds_list()
        self.enemy_list = self.factory.init_enemies_list()
        self.reward = 0
        self.collision = False
        self.agent_is_below_enemy = False
        self.isDown = False
        self.canjump = False
        self.last_jump = None
        self.last_jump2 = None
        self.total_scrool = 0

    def can_jump(self):
        return self.physique_engine.can_jump()



class Policy:  # Q-table  (self, states de l'environnement, actions <<up, down>>)
    def __init__(self, actions,
                 learning_rate=DEFAULT_LEARNING_RATE,
                 discount_factor=DEFAULT_DISCOUNT_FACTOR):
        self.actions = actions
        self.table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

    def best_action(self, state):#state = position de dino (x,y)
        if not state in self.table: # c'est-a-dire self.table[dinoState] est vide
            self.table[state] = {}
            for a in self.actions:
                self.table[state][a] = 0

        action = None
        if bool(self.table): #check if table in not empty due to environment states update
            for a in self.table[state]:
                if action is None or self.table[state][a] > self.table[state][action]:
                    action = a
        return action

    def update(self, previous_state, state, last_action, reward, learning_rate):

        if not state in self.table:
            self.table[state] = {}
            for action in self.actions:
                self.table[state][action] = REWARD_DEFAULT
                if action == UP:
                    self.table[state][action] = REWARD_UP
                elif action == DOWN:
                    self.table[state][action] = REWARD_DOWN

        maxQ = max(self.table[state].values())

        self.table[previous_state][last_action] += learning_rate * \
                                                   (reward + self.discount_factor * maxQ - self.table[previous_state][
                                                       last_action])




