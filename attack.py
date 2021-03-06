import pygame
import numpy
import math

from sprites.projectile import Projectile

class Attack:
    eventCounter = 0

    def __init__(self, projectileImg: pygame.Surface, nbProjectiles: int, projectileSpeed: int, rotateSpeed: float, initialRotation: float, shotCooldownMs: int, projectileWidth = None):
        self.projectileImg = projectileImg
        self.nbProjectiles = nbProjectiles
        self.projectileSpeed = projectileSpeed
        self.rotateSpeed = rotateSpeed
        self.initialRotation = initialRotation
        self.shotCooldownMs = shotCooldownMs
        self.projectileWidth = projectileWidth


    def createShotTimer(self) -> int:
        eventId = pygame.USEREVENT + 10000 + Attack.eventCounter
        Attack.eventCounter += 1
        pygame.time.set_timer(eventId, self.shotCooldownMs)
        return eventId


    def removeShotTimer(self, eventId: int) -> None:
        pygame.time.set_timer(eventId, 0)


    def performAttack(self, gameWorldSurf: pygame.Surface, casterRect: pygame.Rect, projectileGroup: pygame.sprite.Group) -> None:
        rotation = self.initialRotation
        for _ in range(self.nbProjectiles):
            cosTheta = math.cos(rotation)
            sinTheta = math.sin(rotation)

            speed = pygame.math.Vector2(cosTheta, sinTheta) * self.projectileSpeed
            
            projectileSpeed = speed * speed.magnitude()
            projectileSpeed.x = projectileSpeed.x
            projectileSpeed.y = projectileSpeed.y

            projectile = Projectile(gameWorldSurf, self.projectileImg, projectileSpeed, centerx=casterRect.centerx, bottom=casterRect.bottom, width=self.projectileWidth)
            projectileGroup.add(projectile)

            rotation += self.rotateSpeed