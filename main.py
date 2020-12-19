from src.environment import *
from src.game_objects import *
import os
import csv

class Agent(Game_object):
    def __init__(self, environment):
        image_source = "images/dinosaur_frame2.png"
        super().__init__(image_source, CHARACTER_SCALING)

        self.policy = Policy(ACTIONS)
        self.environment = environment
        self.donum = 0
        self.reward = 0
        self.center_x = 64
        self.center_y = 128
        self.state = self.get_state()
        self.previous_state = self.state
        self.previous_state3 = self.state
        self.previous_state2 = self.state
        self.foot = 'left'
        self.last_action = 'W'
        self.last_action2 = self.last_action
        self.last_action3 = self.last_action


    def get_state(self):
        next_enemy = self.environment.enemy_list.get_min_x()
        return (int(self.center_x), int(self.center_y), next_enemy.center_x, next_enemy.center_y)

    def starting_point(self):
        self.center_x = 64
        self.center_y = 128
        self.reset()

    def walk(self):
        if self.foot == 'left':
            texture = arcade.load_texture("images/dinosaur_frame2.png")
        else:
            texture = arcade.load_texture("images/dinosaur_frame3.png")
        self.center_x = 64
        self.texture = texture


    def down(self):
        if self.foot == 'left':
            texture = arcade.load_texture("images/dinosaur_frame5.png")
        else:
            texture = arcade.load_texture("images/dinosaur_frame4.png")
        self.center_x = 64
        self.texture = texture

    def reset(self):
        self.state = (int(self.center_x), int(self.center_y), 0, 0)
        self.environment.reset()
        self.score = 0


    def best_action(self):
        return self.policy.best_action(self.state)

    def do(self, action):
        self.previous_state3 = self.previous_state2
        self.previous_state2 = self.previous_state
        self.previous_state = self.state

        self.state = self.get_state()
        self.reward = self.environment.apply(action)
        self.score += self.reward

        self.last_action3 = self.last_action2
        self.last_action2 = self.last_action
        self.last_action = action

        self.donum += 1


    def update_policy(self):
        self.policy.update(self.previous_state, self.state, self.last_action, self.reward, self.policy.learning_rate)

    def get_with_by_last_action(self):
        withHeightAgent = [128, 128]
        if self.last_action == 'D':
            withHeightAgent = [128, 64]
        return withHeightAgent

    def get_center_y(self):
        agent_height = self.get_with_by_last_action()[1]
        if agent_height == 64:
            agent_center_y = self.center_y - (self.height // 2)
        else:
            agent_center_y = self.center_y
        return agent_center_y

class Window(arcade.Window):
    def __init__(self, agent):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.player_list = None
        self.agent = agent
        self.stage = 0
        arcade.set_background_color(arcade.csscolor.WHITE)
        self.dead = 0
        self.max_score = 0
        self.test = 0


    def setup(self):
        self.player_list = arcade.SpriteList()
        self.agent.starting_point()
        self.player_list.append(self.agent)
        self.agent.environment.setup(self.agent)
        self.testbool = True

    def on_draw(self):
        arcade.start_render()
        self.agent.environment.ground_list.draw()
        self.agent.environment.enemy_list.draw()
        self.player_list.draw()
        arcade.draw_text(f"Score: {self.agent.score}", 10, 10, arcade.csscolor.BLACK, 20)

    def on_update(self, delta_time):
        self.agent.environment.physique_engine.update()
        self.agent.environment.update()
        self.stage += 1

        if self.stage % 10 == 0:
            self.agent.foot = "right"
        else:
            self.agent.foot = "left"

        state = self.agent.get_state()

        if self.agent.environment.collision:
            self.agent.reward = REWARD_STUCK
            self.agent.update_policy()
            if self.max_score < self.agent.score:
                self.max_score = self.agent.score
            self.agent.environment.collision = False
            print(str(self.dead) + " : " + str(self.agent.last_action))
            self.agent.reset()
            self.dead += 1

        if self.stage % 5 == 0 or state[2] == 224:
            if self.agent.environment.can_jump():
                action = self.agent.best_action()
                self.agent.do(action)
                self.agent.update_policy()

    def save_q_table(self):
        save_name = "q_table.csv"
        if os.path.exists(save_name):
            os.remove(save_name)
        w = csv.writer(open(save_name, "w"))
        for key, val in self.agent.policy.table.items():
            w.writerow([key, val])

def main():
    """ Main method """
    env = Environment()
    agent = Agent(env)
    window = Window(agent)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
