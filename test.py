from random import randrange as rnd
from itertools import cycle
from random import choice
from PIL import  Image
# import pygame
import time




# extracting game items and characters form the resource.png image.
player_init = Image.open("resources.png").crop((77,5,163,96)).convert("RGBA")
player_init = player_init.resize(list(map(lambda x:x//2 , player_init.size)))

player_frame_1 = Image.open("resources.png").crop((1679,2,1765,95)).convert("RGBA")
player_frame_1 = player_frame_1.resize(list(map(lambda x:x//2 , player_frame_1.size)))
player_frame_1.save("./")

player_frame_2 = Image.open("resources.png").crop((1767,2,1853,95)).convert("RGBA")
player_frame_2 = player_frame_2.resize(list(map(lambda x:x//2 , player_frame_2.size)))

player_frame_3 = Image.open("resources.png").crop((1855,2,1941,95)).convert("RGBA")
player_frame_3 = player_frame_3.resize(list(map(lambda x:x//2 , player_frame_3.size)))

player_frame_31 = Image.open("resources.png").crop((1943,2,2029,95)).convert("RGBA")
player_frame_31 = player_frame_31.resize(list(map(lambda x:x//2 , player_frame_31.size)))

player_frame_4 = Image.open("resources.png").crop((2030,2,2117,95)).convert("RGBA")
player_frame_4 = player_frame_4.resize(list(map(lambda x:x//2 , player_frame_4.size)))

player_frame_5 = Image.open("resources.png").crop((2207,2,2323,95)).convert("RGBA")
player_frame_5 = player_frame_5.resize(list(map(lambda x:x//2 , player_frame_5.size)))

player_frame_6 = Image.open("resources.png").crop((2324,2,2441,95)).convert("RGBA")
player_frame_6 = player_frame_6.resize(list(map(lambda x:x//2 , player_frame_6.size)))
#
# cloud = Image.open("resources.png").crop((166,2,257,29)).convert("RGBA")
# cloud = cloud.resize(list(map(lambda x:x//2 , cloud.size)))
#
# ground = Image.open("resources.png").crop((2,102,2401,127)).convert("RGBA")
# ground = ground.resize(list(map(lambda x:x//2 , ground.size)))
#
# obstacle1 = Image.open("resources.png").crop((446,2,479,71)).convert("RGBA")
# obstacle1 = obstacle1.resize(list(map(lambda x:x//2 , obstacle1.size)))
#
# obstacle2 = Image.open("resources.png").crop((446,2,547,71)).convert("RGBA")
# obstacle2 = obstacle2.resize(list(map(lambda x:x//2 , obstacle2.size)))
#
# obstacle3 = Image.open("resources.png").crop((446,2,581,71)).convert("RGBA")
# obstacle3 = obstacle3.resize(list(map(lambda x:x//2 , obstacle3.size)))
#
# obstacle4 = Image.open("resources.png").crop((653,2,701,101)).convert("RGBA")
# obstacle4 = obstacle4.resize(list(map(lambda x:x//2 , obstacle4.size)))
#
# obstacle5 = Image.open("resources.png").crop((653,2,701,101)).convert("RGBA")
# obstacle5 = obstacle5.resize(list(map(lambda x:x//2 , obstacle5.size)))
#
# obstacle5 = Image.open("resources.png").crop((653,2,749,101)).convert("RGBA")
# obstacle5 = obstacle5.resize(list(map(lambda x:x//2 , obstacle5.size)))
#
# obstacle6 = Image.open("resources.png").crop((851,2,950,101)).convert("RGBA")
# obstacle6 = obstacle6.resize(list(map(lambda x:x//2 , obstacle6.size)))
