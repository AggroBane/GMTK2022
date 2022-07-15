import pygame
from constants import WIDTH, HEIGHT
from sprites import Player, PlayerProjectileGroup


class Level:
    def __init__(self, num: int, screen: pygame.Surface, background: pygame.Surface) -> None:
        self.num = num
        self.screen = screen
        self.background = background
        self.playerProjectileGroup = PlayerProjectileGroup()
        self.player = Player(pygame.image.load("res/player.png"), self.playerProjectileGroup, center=(WIDTH / 2, HEIGHT / 2))


    def update(self, events, keys) -> None:
        self.pollInput(events, keys)
        self.player.update(events, keys)
        self.playerProjectileGroup.update()


    def draw(self) -> None:
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.player.image, self.player.rect)

        for sprite in self.playerProjectileGroup.sprites():
            self.screen.blit(sprite.image, sprite.rect)


    def pollInput(self, events, keys) -> None:
        pass


def loadLevel(screen: pygame.Surface, levelNum: int) -> Level:
    background = pygame.image.load(f"res/{levelNum}.png")
    level = Level(levelNum, screen, background)
    return level