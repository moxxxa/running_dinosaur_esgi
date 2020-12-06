import arcade
from src.global_variables import *
from src.environment import *
from src.game_objects import *
import random

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
        texture = arcade.load_texture("images/dinosaur_frame2.png")
        self.center_x = 64
        self.texture = texture

    def down(self):
        texture = arcade.load_texture("images/dinosaur_frame4.png")
        self.center_x = 75
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





class Window(arcade.Window):
    def __init__(self, agent):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.player_list = None
        self.agent = agent
        self.stage = 0
        arcade.set_background_color(arcade.csscolor.WHITE)
        self.dead = 0

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.agent.starting_point()
        self.player_list.append(self.agent)
        self.agent.environment.setup(self.agent)

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
            if self.agent.environment.can_jump():
                action = self.agent.best_action()
                self.agent.do(action)
                self.agent.update_policy()

        if self.agent.environment.collision:
            self.agent.reward = REWARD_STUCK
            self.agent.update_policy()
            self.agent.environment.collision = False
            self.agent.reset()
            self.dead += 1
            print("dead : " + str(self.dead))
            print(self.agent.state)
            print(self.agent.previous_state)
            print(self.agent.previous_state2)
            print(self.agent.previous_state3)
            print(self.agent.reward)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if  self.agent.environment.physique_engine.can_jump():
                self.agent.change_y = PLAYER_JUMP_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.agent.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.agent.change_x = 0



def main():
    """ Main method """
    env = Environment()
    agent = Agent(env)
    window = Window(agent)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
