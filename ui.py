import pygame
import pygame_menu
import os
from math import floor
from anim.spritesheet import SpriteSheet
from constants import HEATWAVE_INTERVAL_SEC, WHITE, WIDTH, HEIGHT, RED, PLAYER_LIVES
from utils import resource_path


class UI:
    def __init__(self) -> None:
        self.pixelFont = pygame.font.Font(resource_path(os.path.join("res", "fonts", 'PressStart2P.ttf')), 36)
        self.diceSprite = SpriteSheet("res/dice.png", 128, 128)
        self.timerSprite = SpriteSheet("res/timer.png", 128, 128)
        self.frostMeterSprite = SpriteSheet("res/frostometer.png", 64, 512)
        self.warningSprite = SpriteSheet("res/warning.png", 32, 32)
        self.heartSprite = SpriteSheet("res/iceHeart.png", 128, 128)


        # Setup sounds
        self.heatwaveSound = pygame.mixer.Sound(resource_path("res/heatwave1.mp3"))
        self.dieSound = pygame.mixer.Sound(resource_path("res/playerHit1.mp3"))

        # Sound volumes
        pygame.mixer.Sound.set_volume(self.heatwaveSound,0.35)

    def draw(self, surface: pygame.Surface, frostAmount: int, heatwave: list, lastHeatwave: int, playerLives: int, tutorialPhase: int, tutorialStep: int, num) -> None:
        # Draw right UI
        self.rightUi = pygame.Surface((WIDTH/4, HEIGHT))
        self.rightUiRect = self.rightUi.get_rect(topright=(WIDTH, 0))

        # Draw left UI
        self.leftUi = pygame.Surface((WIDTH/4, HEIGHT))
        self.leftUiRect = self.leftUi.get_rect(topleft=(0, 0))


        if tutorialPhase >= 1: 
            self.drawFrostOMeter(frostAmount)

        if tutorialPhase >= 2: 
            self.drawDice(heatwave)

        self.drawLives(playerLives)

        timeNextHeatwave = self.timeUntilNextHeatwave(lastHeatwave)


        if num != 0:
            self.drawTimer(surface, timeNextHeatwave, heatwave)
        elif (tutorialPhase == 2 and tutorialStep == 1) or tutorialPhase > 2:
            self.drawTimer(surface, timeNextHeatwave, heatwave)



        if (timeNextHeatwave < 2000) and (sum(heatwave) > 0) and (timeNextHeatwave > 1975):
            pygame.mixer.Sound.play(self.heatwaveSound)

        if (timeNextHeatwave < 2000) and (sum(heatwave) > 0):
            # Gamescreen surface
            heatwaveSurf = pygame.Surface((WIDTH/2, HEIGHT))
            heatwaveRect = heatwaveSurf.get_rect(center=(WIDTH/2, HEIGHT/2))

            heatwaveSurf.fill(RED)

            

            # Set greater opacity the closer you get to 0
            max_opacity = 100  # Solid block is 255
            heatwaveSurf.set_alpha(int(max_opacity - (timeNextHeatwave / 20)))
            surface.blit(heatwaveSurf, heatwaveRect)

        surface.blit(self.rightUi, self.rightUiRect)
        surface.blit(self.leftUi, self.leftUiRect)

        self.drawBorder(surface)

    def drawFrostOMeter(self,  frostAmount) -> None:
        frostMeter = self.frostMeterSprite.image_at(frostAmount - 1, 0, -1)
        frostMeterRect = frostMeter.get_rect()
        frostMeterRect.centery = self.rightUiRect.centery
        frostMeterRect.left += 50

        frostText = self.pixelFont.render(
            str(int(frostAmount)), True, (255, 255, 255))
        frostTextRect = frostText.get_rect()
        frostTextRect.centerx = frostMeterRect.centerx
        frostTextRect.top = frostMeterRect.bottom + 25

        self.rightUi.blit(frostText, frostTextRect)

        self.rightUi.blit(frostMeter, frostMeterRect)

    def drawDice(self, heatwave: list) -> None:
        diceYOffset = 16
        diceYStart = HEIGHT - diceYOffset

        for i in range(len(heatwave)):
            diceImage = self.diceSprite.image_at(heatwave[i], 0, -1)
            diceRect = diceImage.get_rect()
            diceRect.right = self.leftUiRect.right - 50
            diceRect.bottom = diceYStart - (i * (128 + diceYOffset))

            self.leftUi.blit(diceImage, diceRect)

        pass

    # Returns the time left until the next heatwave in ms
    def timeUntilNextHeatwave(self, lastHeatwave: int) -> int:
        return HEATWAVE_INTERVAL_SEC * 1000 + lastHeatwave - pygame.time.get_ticks()

    def drawTimer(self, screen: pygame.surface, timeLeft: int, heatwave: list) -> None:
        secondsLeft = int(timeLeft / 1000)
        timerImage = self.timerSprite.image_at(
            secondsLeft % 8, 0, -1)
        timerRect = timerImage.get_rect()
        timerRect.right = self.leftUiRect.right - 50
        timerRect.top = 100

        timerText = self.pixelFont.render(
            str(int(secondsLeft)), True, (255, 255, 255))
        timerTextRect = timerText.get_rect()
        timerTextRect.centerx = timerRect.centerx
        timerTextRect.top = timerRect.bottom + 25

        if (secondsLeft < 4 and sum(heatwave) > 0):
            warningText = self.pixelFont.render(
                'HEATWAVE INCOMING', True, RED)
            warningTextRect = warningText.get_rect()
            warningTextRect.centerx = WIDTH/2
            warningTextRect.top = 100

            screen.blit(warningText, warningTextRect)

            if (floor(timeLeft / 500 % 2) == 0):
                warningIcon = self.warningSprite.image_at(0, 0, -1)
                leftWarningRect = warningIcon.get_rect()
                rightWarningRect = warningIcon.get_rect()

                leftWarningRect.centery = warningTextRect.centery
                rightWarningRect.centery = warningTextRect.centery

                leftWarningRect.right = warningTextRect.left - 25
                rightWarningRect.left = warningTextRect.right + 25

                screen.blit(warningIcon, leftWarningRect)
                screen.blit(warningIcon, rightWarningRect)

        self.leftUi.blit(timerText, timerTextRect)
        self.leftUi.blit(timerImage, timerRect)

    def drawLives(self, nbLives):
        offsetHeart = 25
        heartSize = 128
        surfHeight = (heartSize + offsetHeart)*PLAYER_LIVES
        heartSurface = pygame.Surface((heartSize, surfHeight))

        for i in range(PLAYER_LIVES):

            y_offset = int(i * (heartSize + offsetHeart))

            if nbLives >= 1:
                heartSurface.blit(self.heartSprite.image_at(
                    0, 0, -1), (0, y_offset))
                nbLives -= 1
            else:
                heartSurface.blit(self.heartSprite.image_at(
                    1, 0, -1), (0, y_offset))

        heartRect = heartSurface.get_rect()
        heartRect.centerx = self.leftUiRect.centerx + 50
        heartRect.centery = self.rightUiRect.centery

        self.rightUi.blit(heartSurface, heartRect)

    def drawBorder(self, surface: pygame.Surface) -> None:
        borderSurface = pygame.Surface((32, HEIGHT))
        borderSurface.fill(WHITE)

        borderRect = borderSurface.get_rect()
        borderRect.left = self.rightUiRect.left - 10

        surface.blit(borderSurface, borderRect)

        borderRect.right = self.leftUiRect.right + 10
        surface.blit(borderSurface, borderRect)
