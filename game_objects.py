import random
from operator import attrgetter
import numpy

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
        pass

    def createBird(self):
        bird = GameObject()
        bird.sprite = ["bird1.png", "bird2.png"]
        b = random.randint(0, 2)
        if b != 0:
            bird.y = 380
        bird.y = 380
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

        return self.createBird()
