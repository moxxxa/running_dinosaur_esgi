import arcade
import arcade
from src.global_variables import *

class Game_object(arcade.Sprite):
    def __init__(self, image_source, scaling):
        super().__init__(image_source, scaling)
        self.updateNum = 0

    def collisionX(self, other_game_object):

        x_min = self.center_x - self.width // 2
        x_max = self.center_x + self.width // 2

        x_min_agent = other_game_object.center_x - other_game_object.get_width() // 2
        x_max_agent = other_game_object.center_x + other_game_object.get_width() // 2

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

    def get_width(self):
        return self.width


    def update_animation(self, delta_time: float = 1/60):
        print("salut")


class Game_object_factory():
    def __init__(self):
        pass

    def init_grounds_list(self):
        image_source = "images/ground.png"
        ground_list = listWall()

        wall = Game_object(image_source, TILE_SCALING)

        for x in range(0, int(wall.width * 3), int(wall.width)):
            wall = Game_object(image_source, TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            ground_list.append(wall)

        return ground_list

    def init_clouds_list(self):
        image_source = "images/clouds.png"
        clouds_list = listWall()

        wall = Game_object(image_source, TILE_SCALING)

        for x in range(0, int(wall.width * 3), int(wall.width)):
            wall = Game_object(image_source, TILE_SCALING)
            wall.center_x = x
            wall.center_y = 350
            clouds_list.append(wall)

        return clouds_list

    def init_enemies_list(self):
        image_source = "images/bird1.png"
        enemy_list = listWall()

        wall = Game_object(image_source, ENEMY_SCALING)
        wall.center_x = 2560
        wall.center_y = 120
        enemy_list.append(wall)

        wall = Game_object(image_source, ENEMY_SCALING)
        wall.center_x = 1280
        wall.center_y = 200
        enemy_list.append(wall)

        return enemy_list

    def init_bird(self):
        image_source = "images/grassHalf_mid.png"
        ground_list = listWall()
        for x in range(-64, 1344, 64):
            wall = Game_object(image_source, TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            ground_list.append(wall)
        return ground_list




class listWall(arcade.SpriteList):
    def __init__(self):
        super().__init__(use_spatial_hash=True)
        self.scroolValue = 0

        self.delete = False

    def scrool(self):
        self.scroolObject(SCROOL_SPEED)

    def scroolObject(self, speed):
        for i in range(0, len(self.sprite_list)):
            self.sprite_list[i].center_x -= speed
            self.scroolValue += speed

    def pop(self, center_x):
        for i in range(0, len(self.sprite_list)):
            if self.sprite_list[i].center_x < self.sprite_list[i].width * -1:
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

        next_enemy = self.get_min_x()

        mob = next_enemy.collisionX(agent)
        mob = mob or agent.collisionX(next_enemy)

        return mob

    def colYWithAgent(self, agent):
        next_enemy = self.get_min_x()
        mob = next_enemy.collisionY(agent)
        mob = mob or agent.collisionY(next_enemy)
        return mob



