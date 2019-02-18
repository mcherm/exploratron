
import pygame
from message import MessagePainter
from images import TILE_SIZE
from inventory_view import LocalInventoryView, RemoteInventoryView
from clientdata import GridData, InventoryData
from exploranetworking import RequestInventoryMessage



class PygameGridDisplay:
    def __init__(self, screen):
        self.screen = screen

    def show(self, gridData, uiState, imageLibrary):
        assert isinstance(gridData, GridData)
        self.screen.fill((0, 0, 0))
        screenWidth, screenHeight = uiState.screenWidthAndHeight
        for screenY in range(min(screenHeight, gridData.height)):
            for screenX in range(min(screenWidth, gridData.width)):
                offsetX, offsetY = uiState.offset
                cellData = gridData.cellAt(screenX + offsetX, screenY + offsetY)
                for tileId in cellData.tileIds():
                    image = imageLibrary.lookupById(tileId)
                    self.screen.blit(image, (TILE_SIZE * screenX, TILE_SIZE * screenY))


LIGHT_GREY = (120, 120, 120)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
PURPLE = (144, 9, 189)


class PygameOverlayDisplay:
    """This manages rendering UI components in the display."""

    def __init__(self, surface):
        self.surface = surface
        self.messagePainter = MessagePainter()

    def show(self, uiState, imageLibrary):
        # health and mana bars
        if uiState.visibleData:
            BAR_SPACE = 5
            BAR_BORDER = 1
            BAR_WIDTH = 16
            SCALE = 10
            FULL_BORDER = BAR_BORDER + BAR_SPACE
            MANA_OFFSET = FULL_BORDER + BAR_WIDTH + BAR_BORDER

            #create health bar
            maxHealth = uiState.visibleData.maxHealth
            health = uiState.visibleData.health
            healthBorderRect = pygame.Rect(BAR_SPACE, BAR_SPACE, maxHealth * SCALE + 2 * BAR_BORDER,
                                     BAR_WIDTH + 2 * BAR_BORDER)
            maxHealthRect = pygame.Rect(FULL_BORDER, FULL_BORDER, maxHealth * SCALE, BAR_WIDTH)
            healthRect = pygame.Rect(FULL_BORDER, FULL_BORDER, health * SCALE, BAR_WIDTH)
            self.surface.fill(BLACK, healthBorderRect)
            self.surface.fill(LIGHT_GREY, maxHealthRect)
            self.surface.fill(RED, healthRect)

            #create mana bar
            maxMana = uiState.visibleData.maxMana
            mana = uiState.visibleData.mana
            manaBorderRect = pygame.Rect(BAR_SPACE, BAR_SPACE + MANA_OFFSET, maxMana * SCALE + 2 * BAR_BORDER,
                                     BAR_WIDTH + 2 * BAR_BORDER)
            maxManaRect = pygame.Rect(FULL_BORDER, FULL_BORDER + MANA_OFFSET, maxMana * SCALE, BAR_WIDTH)
            manaRect = pygame.Rect(FULL_BORDER, FULL_BORDER + MANA_OFFSET, mana * SCALE, BAR_WIDTH)
            self.surface.fill(BLACK, manaBorderRect)
            self.surface.fill(LIGHT_GREY, maxManaRect)
            self.surface.fill(PURPLE, manaRect)

        # Messages
        if uiState.message:
            self.messagePainter.paintMessage(self.surface, uiState.message)

        # inventory
        if uiState.inventoryView:
            uiState.inventoryView.show(self.surface, imageLibrary)


class PygameDisplay:
    """This is an object which will render the game, using the pygame library.
    It has two basic layers: a PygameGridDisplay which renders the room you
    are in, and an PygameOverlayDisplay which shows UI components over top
    of the grid. It also deals with playing sounds."""

    def __init__(self):
        STARTING_WIDTH_IN_TILES = 16
        STARTING_HEIGHT_IN_TILES = 11
        self.uiState = UIState(STARTING_WIDTH_IN_TILES, STARTING_HEIGHT_IN_TILES)
        self.screen = pygame.display.set_mode(
            (STARTING_WIDTH_IN_TILES * TILE_SIZE, STARTING_HEIGHT_IN_TILES * TILE_SIZE))
        pygame.event.set_allowed(None)
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])

        self.gridDisplay = PygameGridDisplay(self.screen)
        self.overlayDisplay = PygameOverlayDisplay(self.screen)

    def show(self, gridData, imageLibrary):
        self.gridDisplay.show(gridData, self.uiState, imageLibrary)
        self.overlayDisplay.show(self.uiState, imageLibrary)
        pygame.display.flip()

    def playSounds(self, soundEffectIds, soundLibrary):
        """Causes the display to begin playing each of the sounds whose sound effect
        ID is in the list provided."""
        for soundEffectId in soundEffectIds:
            sound = soundLibrary.lookupById(soundEffectId)
            sound.play()

    def setDisplayedPlayerId(self, playerId):
        self.uiState.setDisplayedPlayerId(playerId)

    def setVisibleData(self, visibleData):
        """Call this to update the continually-displayed visible data."""
        self.uiState.setVisibleData(visibleData)

    def getEvents(self):
        return pygame.event.get()

    def quit(self):
        pygame.quit()


class UIState:
    """This class contains information about the current state of controls that
    make up the UI. That includes, for instance, the camera position."""

    def __init__(self, initialScreenWidth, initialScreenHeight,):
        """Initialize a UIState. Caller must specify initial screen width and height
        are measured in TILES, not pixels."""
        self.playerId = None
        self.screenWidthAndHeight = initialScreenWidth, initialScreenHeight
        self.roomWidthAndHeight = 0, 0
        self.offset = 0, 0
        self.visibleData = None
        self.inventoryView = None
        self.message = None # a single Message object that is shown until the user clears it

    def setDisplayedPlayerId(self, playerId):
        self.playerId = playerId

    def setVisibleData(self, visibleData):
        """Call this to update the continually-displayed visible data."""
        self.visibleData = visibleData

    def newRoom(self, gridData):
        assert isinstance(gridData, GridData)
        self.roomWidthAndHeight = gridData.width, gridData.height
        self.offset = 0, 0

    def moveCrosshairTo(self, newPosition):
        """Moves the crosshair position to the given (x,y) location (in pixels)."""
        self.crosshairPosition = newPosition

    def moveCrosshairBy(self, deltaPosition):
        """Given (deltaX, deltaY) in pixels, moves the crosshair by that amount."""
        self.crosshairPosition = (
            self.crosshairPosition[0] + deltaPosition[0],
            self.crosshairPosition[1] + deltaPosition[1])

    def moveUISouth(self):
        if self.inventoryView:
            self.inventoryView.moveCrosshairSouth()
        else:
            x, y = self.offset
            offsetY = self.offset[1]
            screenY = self.screenWidthAndHeight[1]
            roomY = self.roomWidthAndHeight[1]
            if roomY > screenY + offsetY:
                self.offset = x, y + 1

    def moveUINorth(self):
        if self.inventoryView:
            self.inventoryView.moveCrosshairNorth()
            if self.inventoryView.shouldExit:
                self.inventoryView = None
        else:
            x, y = self.offset
            offsetY = self.offset[1]
            if offsetY > 0:
                self.offset = x, y - 1

    def moveUIEast(self):
        if self.inventoryView:
            self.inventoryView.moveCrosshairEast()
        else:
            x, y = self.offset
            offsetX = self.offset[0]
            screenX = self.screenWidthAndHeight[0]
            roomX = self.roomWidthAndHeight[0]
            if roomX > screenX + offsetX:
                self.offset = x + 1, y

    def moveUIWest(self):
        if self.inventoryView:
            self.inventoryView.moveCrosshairWest()
        else:
            x, y = self.offset
            offsetX = self.offset[0]
            screenX = self.screenWidthAndHeight[0]
            roomX = self.roomWidthAndHeight[0]
            if offsetX > 0:
                self.offset = x - 1, y

    def takeAction(self):
        """This is called when someone presses the UI action button."""
        if self.inventoryView:
            self.inventoryView.takeAction()
        elif self.message is not None:
            self.message = None
        else:
            pass

    def toggleInventoryLocal(self, player):
        """Toggle whether the inventory is displayed. This version is intended for use
        in a local display where the actual player object is available for performing
        actions like drop and equip."""
        if player:
            if self.inventoryView is None:
                self.inventoryView = LocalInventoryView(player)
            else:
                self.inventoryView = None
        else:
            # There is no player, so we can't show inventory
            self.inventoryView = None

    def toggleInventoryRemote(self, clientsideConnection):
        """Toggle whether the inventory is displayed.

        For the moment, during a cleanup, there are two different versions of this,
        one for the local server and one for a remote viewer. I hope to fix that
        eventually."""
        if self.playerId:
            if self.inventoryView is None:
                clientsideConnection.send(RequestInventoryMessage())
            else:
                self.inventoryView = None
        else:
            # There is no player, so we can't show inventory
            self.inventoryView = None

    def showInventoryRemote(self, clientsideConnection, inventoryData):
        """Begin showing an inventory. This is used by the remote view once
        an inventory becomes available."""
        self.inventoryView = RemoteInventoryView(clientsideConnection, inventoryData)

