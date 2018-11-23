
import pygame
from images import TILE_SIZE
from inventory_view import drawInventory



class PygameGridDisplay:
    def __init__(self):
        SCREEN_WIDTH_IN_TILES = 16
        SCREEN_HEIGHT_IN_TILES = 11
        self.uiState = UIState(SCREEN_WIDTH_IN_TILES, SCREEN_HEIGHT_IN_TILES)
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH_IN_TILES * TILE_SIZE, SCREEN_HEIGHT_IN_TILES * TILE_SIZE))
        pygame.event.set_allowed(None)
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])

    def show(self, room, imageLibrary):
        self.screen.fill((0, 0, 0))
        screenWidth, screenHeight = self.uiState.screenWidthAndHeight
        for screenY in range(min(screenHeight, room.height)):
            for screenX in range(min(screenWidth, room.width)):
                offsetX, offsetY = self.uiState.offset
                cell = room.cellAt(screenX + offsetX, screenY + offsetY)
                for thing in cell.things:
                    image = imageLibrary.lookupById(thing.tileId)
                    self.screen.blit(image, (TILE_SIZE * screenX, TILE_SIZE * screenY))


LIGHT_GREY = (120, 120, 120)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


class PygameOverlayDisplay:
    """This manages rendering UI components in the display."""

    def __init__(self, surface):
        self.surface = surface

    def show(self, uiState, imageLibrary):
        # health bar
        if uiState.player:
            BAR_SPACE = 5
            BAR_BORDER = 1
            BAR_WIDTH = 16
            SCALE = 10
            FULL_BORDER = BAR_BORDER + BAR_SPACE

            maxHealth = uiState.player.stats.maxHealth
            health = uiState.player.stats.health
            borderRect = pygame.Rect(BAR_SPACE, BAR_SPACE, maxHealth * SCALE + 2 * BAR_BORDER,
                                     BAR_WIDTH + 2 * BAR_BORDER)
            maxHealthRect = pygame.Rect(FULL_BORDER, FULL_BORDER, maxHealth * SCALE, BAR_WIDTH)
            healthRect = pygame.Rect(FULL_BORDER, FULL_BORDER, health * SCALE, BAR_WIDTH)
            self.surface.fill(BLACK, borderRect)
            self.surface.fill(LIGHT_GREY, maxHealthRect)
            self.surface.fill(RED, healthRect)

        # inventory
        if uiState.showInventory:
            drawInventory(uiState.player.inventory, self.surface, imageLibrary)


class PygameDisplay:
    """This is an object which will render the game, using the pygame library.
    It has two basic layers: a PygameGridDisplay which renders the room you
    are in, and an PygameOverlayDisplay which shows UI components over top
    of the grid. It also deals with playing sounds."""

    def __init__(self):
        self.gridDisplay = PygameGridDisplay()
        # FIXME: The surface should be owned by the PygameDisplay, not the GridDisplay.
        self.overlayDisplay = PygameOverlayDisplay(self.gridDisplay.screen)

    @property
    def uiState(self):
        return self.gridDisplay.uiState  # Should move uiState to PygameDisplay, not GridDisplay

    def show(self, room, imageLibrary):
        self.gridDisplay.show(room, imageLibrary)
        self.overlayDisplay.show(self.gridDisplay.uiState, imageLibrary)
        pygame.display.flip()

    def playSounds(self, soundEffectIds, soundLibrary):
        """Causes the display to begin playing each of the sounds whose sound effect
        ID is in the list provided."""
        for soundEffectId in soundEffectIds:
            sound = soundLibrary.lookupById(soundEffectId)
            sound.play()

    def setDisplayedPlayer(self, player):
        self.uiState.setDisplayedPlayer(player)

    def getEvents(self):
        return pygame.event.get()

    def quit(self):
        pygame.quit()


class UIState:
    """This class contains information about the current state of controls that
    make up the UI. That includes, for instance, the camera position."""

    def __init__(self, initialScreenWidth, initialScreenHeight, player=None):
        """Initialize a UIState. Caller must specify which player is displayed.
        initial screen width and height are measured in TILES, not pixels."""
        self.player = player
        self.screenWidthAndHeight = initialScreenWidth, initialScreenHeight
        self.roomWidthAndHeight = 0, 0
        self.offset = 0, 0
        self.showInventory = False

    def setDisplayedPlayer(self, player):
        self.player = player

    def newRoom(self, room):
        self.roomWidthAndHeight = room.width, room.height
        self.offset = 0, 0

    def moveCameraSouth(self):
        x, y = self.offset
        offsetY = self.offset[1]
        screenY = self.screenWidthAndHeight[1]
        roomY = self.roomWidthAndHeight[1]
        if roomY > screenY + offsetY:
            self.offset = x, y + 1

    def moveCameraNorth(self):
        x, y = self.offset
        offsetY = self.offset[1]
        screenY = self.screenWidthAndHeight[1]
        roomY = self.roomWidthAndHeight[1]
        if offsetY > 0:
            self.offset = x, y - 1

    def moveCameraEast(self):
        x, y = self.offset
        offsetX = self.offset[0]
        screenX = self.screenWidthAndHeight[0]
        roomX = self.roomWidthAndHeight[0]
        if roomX > screenX + offsetX:
            self.offset = x + 1, y

    def moveCameraWest(self):
        x, y = self.offset
        offsetX = self.offset[0]
        screenX = self.screenWidthAndHeight[0]
        roomX = self.roomWidthAndHeight[0]
        if offsetX > 0:
            self.offset = x - 1, y

    def toggleInventory(self):
        if self.player:
            self.showInventory = not self.showInventory
        else:
            # There is no player, so we can't show inventory
            self.showInventory = False

