import random
from operator import attrgetter
import numpy

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Dinosaur runner"
UP, DOWN = 'U', 'D'
ACTIONS = [UP, DOWN]

PREFIX_RESSOURCE = "resources/"

PLAYER_JUMP_SPEED = 20

DINO_SIZE = 0.7

REWARD_STUCK = -6
REWARD_DEFAULT = 1

SCROOL_SPEED = 5

PREFIX_RESSOURCE = "resources/"


def random_case():
    return numpy.random.choice(numpy.arange(1, 10), p=[0.6, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05])

class GameObject():
    def __init__(self):
        self.y = 310
        self.x = 950
        self.frame = 0
        self.scrool = 0
        self.sprite = []
        self.nextObject = None

    def reset(self):
        self.y = 310
        self.x = 950

    def addScrool(self, scroolSpeed):
        self.scrool += scroolSpeed
        if self.scrool % 75 < scroolSpeed:
            self.addFrame()

    def addFrame(self):
        self.frame += 1

    def getCurrentSprite(self):
        frameNum = 0
        if (len(self.sprite) != 0):
            frameNum = self.frame % len(self.sprite)
        return self.sprite[frameNum]


class GameObjectFactory():
    def __init__(self):
        print("init Factory")

    def createBird(self):
        bird = GameObject()
        bird.sprite = ["bird1.png", "bird2.png"]
        b = random.randint(0, 2)
        if b != 0:
            bird.y = 340
        return bird

    def createCactus(self):
        cactus = GameObject()
        cactus.sprite = ["obstacle.png"]
        return cactus

    def createBigCactus(self):
        cactus = GameObject()
        cactus.sprite = ["obstacle2.png"]
        cactus.y = cactus.y + 10
        return cactus

    def createRambdomObject(self):
        rambdomObject = self.createCactus()
        b = random.randint(0, 2)

        if (b == 1):
            rambdomObject = self.createBigCactus()
        elif (b == 2):
            rambdomObject = self.createBird()

        return rambdomObject


class Environment:
    def __init__(self):
        self.states = {}
        self.height = SCREEN_HEIGHT
        self.width = SCREEN_WIDTH
        self.starting_point = (SCREEN_WIDTH / 6, SCREEN_HEIGHT / 2)
        self.gameObject = []
        self.gameObjectFactory = GameObjectFactory()
        self.__spawn_service()
        self.totalScrool = 0

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

    def update(self, scroolSpeed):
        self.__clean()
        self.scrool(scroolSpeed)
        appendNewObstacle = random_case()
        if appendNewObstacle == 7:
            self.__spawn_service()

    def __clean(self):
        if (len(self.gameObject) < 10):
            return
        del self.gameObject[0]
        self.__clean()

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


def test():
    b = GameObjectFactory()

    a = b.createRambdomObject()
    print(a.arcadeGameObject.center_x)

    a.addScrool(3)

    print(a.arcadeGameObject.center_x)

    a.addFrame()
    print(a.getCurrentSprite())

    a.addFrame()
    print(a.getCurrentSprite())
    # obstacles = arcade.SpriteList()
    a.addScrool(10)
