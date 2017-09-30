
import pygame
import os

TILE_SIZE = 64

class ImageLibrary:
    def __init__(self, subdir):
        rootDir = './img'
        self.imageById = {}
        self._idByName = {}
        for root, dirs, files in os.walk(f'{rootDir}/{subdir}'):
            files.sort() # important to sort them so the order is consistent
            counter = 0
            for file in files:
                if file.endswith('.png'):
                    name = f'{subdir}/{file[:-4]}'
                    tileId = counter
                    self._idByName[name] = tileId
                    self.imageById[tileId] = pygame.image.load(f'{rootDir}/{name}.png')
                    counter += 1
    def lookupById(self, imgnum):
        return self.imageById[imgnum]
    def idByName(self, imageName):
        """Pass in an imageName, this returns the tileId for it, or
        raises an exception if that imageName is not known to this
        imageLibrary."""
        return self._idByName[imageName]

    
class PygameGridDisplay:
    def __init__(self):
        SCREEN_WIDTH_IN_TILES = 16
        SCREEN_HEIGHT_IN_TILES = 11
        self.camera = Camera(SCREEN_WIDTH_IN_TILES, SCREEN_HEIGHT_IN_TILES)
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH_IN_TILES*TILE_SIZE, SCREEN_HEIGHT_IN_TILES*TILE_SIZE) )
        pygame.event.set_allowed(None)
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
    def show(self, room, imageLibrary):
        self.screen.fill( (0,0,0) )
        screenWidth, screenHeight = self.camera.screenWidthAndHeight
        for screenY in range(min(screenHeight, room.height)):
            for screenX in range(min(screenWidth, room.width)):
                offsetX, offsetY = self.camera.offset
                cell = room.cellAt(screenX + offsetX, screenY + offsetY)
                for thing in cell.things:
                    image = imageLibrary.lookupById( thing.tileId )
                    self.screen.blit( image, (TILE_SIZE*screenX, TILE_SIZE*screenY) )
        pygame.display.flip()
    def getEvents(self):
        return pygame.event.get()
    def quit(self):
        pygame.quit()


class Camera:
    def __init__(self, screenWidth, screenHeight):
        self.screenWidthAndHeight = screenWidth, screenHeight
        self.roomWidthAndHeight = 0,0
        self.offset = 0,0
    def newRoom(self, room):
        self.roomWidthAndHeight = room.width, room.height
        self.offset = 0,0
    def moveCameraSouth(self):
        x,y = self.offset
        offsetY = self.offset[1]
        screenY = self.screenWidthAndHeight[1]
        roomY = self.roomWidthAndHeight[1]
        if roomY > screenY + offsetY:
            self.offset = x,y+1
    def moveCameraNorth(self):
        x,y = self.offset
        offsetY = self.offset[1]
        screenY = self.screenWidthAndHeight[1]
        roomY = self.roomWidthAndHeight[1]
        if offsetY > 0:
            self.offset = x,y-1
    def moveCameraEast(self):
        x,y = self.offset
        offsetX = self.offset[0]
        screenX = self.screenWidthAndHeight[0]
        roomX = self.roomWidthAndHeight[0]
        if roomX > screenX + offsetX:
            self.offset = x+1,y
    def moveCameraWest(self):
        x,y = self.offset
        offsetX = self.offset[0]
        screenX = self.screenWidthAndHeight[0]
        roomX = self.roomWidthAndHeight[0]
        if offsetX > 0:
            self.offset = x-1,y



class Region:
    """Someday, this might grow into the ability to have different
    regions with their own sets of rooms and their own image libraries."""
    def __init__(self):
        self.imageLibrary = ImageLibrary('drawntiles64')
