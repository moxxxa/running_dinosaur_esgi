import arcade
import arcade
from src.global_variables import *

class Game_object(arcade.Sprite):
    def __init__(self, image_source, scaling):
        super().__init__(image_source, scaling)

    def collisionWithX(self, agent, agent_width):

        x_min = self.center_x - self.width // 2
        x_max = self.center_x + self.width // 2

        x_min_agent = agent.center_x - agent_width // 2
        x_max_agent = agent.center_x + agent_width // 2

        return (x_max_agent > x_min or x_min_agent > x_min) and (x_max_agent < x_max or x_min_agent < x_max)

    def collisionY(self, other_game_object):

        x_min = self.get_center_y() - self.get_height() // 2
        x_max = self.get_center_y() + self.get_height() // 2

        x_min_agent = other_game_object.get_center_y() - other_game_object.get_height() // 2
        x_max_agent = other_game_object.get_center_y() + other_game_object.get_height() // 2

        return (x_min < x_max_agent < x_max) or (x_min < x_min_agent < x_max)

    def get_center_y(self):
        return self.center_y

    def get_height(self):
        return self.height


class Game_object_factory():
    def __init__(self):
        pass

    def init_grounds_list(self):
        image_source = "images/grassHalf_mid.png"
        ground_list = listWall(64)
        for x in range(-64, 1344, 64):
            wall = Game_object(image_source, TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            wall.type = "freindly"
            ground_list.append(wall)
        return ground_list

    def init_enemies_list(self):
        image_source = "images/bird1.png"
        enemy_list = listWall(1280)

        bird1 = Game_object(image_source, ENEMY_SCALING)
        bird1.center_x = 2560
        bird1.center_y = 120
        bird1.type = "enemy"
        enemy_list.append(bird1)

        bird2 = Game_object(image_source, ENEMY_SCALING)
        bird2.center_x = 1280
        bird2.center_y = 200
        bird2.type = "enemy"
        enemy_list.append(bird2)

        return enemy_list


class listWall(arcade.SpriteList):
    def __init__(self, scrollSchedule):
        super().__init__(use_spatial_hash=True)
        self.scroolValue = 0
        self.scroolSchedule = int(scrollSchedule)
        self.delete = False

    def scrool(self, spawn_rate):
        for i in range(0, len(self.sprite_list)):
            if self.sprite_list[i].type == "freindly":
                new_spawn_rate = SCROOL_SPEED
            else:
                new_spawn_rate = SCROOL_SPEED + spawn_rate
            if self.sprite_list[i].type == "enemy":
                print('scroll speed + spawnRate =', new_spawn_rate)
            self.sprite_list[i].center_x -= new_spawn_rate
            self.scroolValue += new_spawn_rate

    def pop(self, center_x):
        for i in range(0, len(self.sprite_list)):
            if self.sprite_list[i].center_x < -64:
                self.sprite_list[i].center_x = center_x

            if self.sprite_list[i].center_x < 0:
                self.delete = True

    def get_min_x(self):
        game_object = self.sprite_list[0]
        for i in range(0, len(self.sprite_list)):
            if self.sprite_list[i].center_x < game_object.center_x and self.sprite_list[i].center_x > -128:
                game_object = self.sprite_list[i]
        return game_object

    def reqardByAction(self, action):
        reward = REWARD_DEFAULT
        if action == UP:
            reward = REWARD_UP
        elif action == DOWN:
            reward = REWARD_DOWN
        return reward

    def colXWithAgent(self, agent):
        mob = self.get_min_x().collisionWithX(agent, agent.get_with_by_last_action()[0])
        mob = mob or agent.collisionWithX(self.get_min_x(), self.get_min_x().width)
        return mob

    def colYWithAgent(self, agent):
        next_enemy = self.get_min_x()
        mob = next_enemy.collisionY(agent)
        mob = mob or agent.collisionY(next_enemy)
        return mob



