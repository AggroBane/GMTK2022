import sys
import pygame
from typing import NamedTuple
from constants import TARGET_FPS, SURFACE_SIZE
from states import InGameState, MenuState, CreditsState, State
from utils import resource_path
from states.endGameState import EndGameState


class Game:
    BACKGROUND_COLOR = (74, 74, 74)

    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode(
            SURFACE_SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF)

        icon = pygame.image.load(resource_path("res/frostoLogo.png")).convert_alpha()
        pygame.display.set_caption('80 Degree Snow')
        pygame.display.set_icon(icon)

        # States
        self.dicStates = {
            InGameState.__name__: InGameState(self, self.screen),
            MenuState.__name__: MenuState(self, self.screen),
            CreditsState.__name__: CreditsState(self, self.screen),
            EndGameState.__name__: EndGameState(self, self.screen)
        }
        self.curState = MenuState.__name__
        self.nextState = None
        self.nextStatePayload = None

        self.clock = pygame.time.Clock()

    def gameLoop(self) -> None:
        while True:
            if (pygame.event.peek(pygame.QUIT)):
                pygame.quit()
                sys.exit()

            keys = pygame.key.get_pressed()
            events = pygame.event.get()

            if self.nextState is not None:
                self.dicStates[self.curState].onExitState()
                self.curState = self.nextState
                self.dicStates[self.curState].onEnterState(
                    self.nextStatePayload)
                self.nextState = None
                self.nextStatePayload = None

            self.screen.fill(Game.BACKGROUND_COLOR)

            self.dicStates[self.curState].update(events, keys)
            self.dicStates[self.curState].draw()

            pygame.display.flip()
            self.clock.tick(TARGET_FPS)

    # Lol its a hackthon fuck this ---> ONLY A STATE OBJECT SHOULD BE ABLE TO SWITCH STATES IF WE WANT TO AVOIR SPAGHETT

    def switchState(self, newStateStr: str, payload: NamedTuple = None) -> None:
        if self.nextState is None and newStateStr in self.dicStates:
            self.nextState = newStateStr
            self.nextStatePayload = payload
        else:
            print("CANT SWITCH STATE")


if __name__ == "__main__":
    Game().gameLoop()
