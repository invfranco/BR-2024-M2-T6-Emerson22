import random

from dino_runner.components.obstacles.obstacle import Obstacle


class Birds(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        self.rect.y = 200
        self.rect.x = 800