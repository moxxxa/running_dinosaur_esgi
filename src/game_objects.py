import arcade
import arcade
from src.global_variables import *

class Game_object(arcade.Sprite):
    def __init__(self, image_source, scaling):

        super().__init__(image_source, scaling)

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
            ground_list.append(wall)
        return ground_list

    def init_enemies_list(self):
        image_source = "images/bird1.png"
        enemy_list = listWall(1280)
        for x in range(1344, 4032, 1344):
            wall = Game_object(image_source, ENEMY_SCALING)
            wall.center_x = x
            wall.center_y = 120
            enemy_list.append(wall)
        return enemy_list

    def init_bird(self):
        image_source = "images/grassHalf_mid.png"
        ground_list = listWall(64)
        for x in range(-64, 1344, 64):
            wall = Game_object(image_source, TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            ground_list.append(wall)
        return ground_list




class listWall(arcade.SpriteList):
    def __init__(self, scrollSchedule):
        super().__init__(use_spatial_hash=True)
        self.scroolValue = 0
        self.scroolSchedule = int(scrollSchedule)
        self.delete = False

    def scrool(self):
        for i in range(0, len(self.sprite_list)):
            self.sprite_list[i].center_x -= SCROOL_SPEED
            self.scroolValue += SCROOL_SPEED

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

