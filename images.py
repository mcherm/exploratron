
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
        self.screen = pygame.display.set_mode( (1024,768) )
        pygame.event.set_allowed(None)
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
    def show(self, room, imageLibrary):
        self.screen.fill( (0,0,0) )
        for y in range(room.height):
            for x in range(room.width):
                cell = room.cellAt(x,y)
                for thing in cell.things:
                    image = imageLibrary.lookupById( thing.tileId )
                    self.screen.blit( image, (TILE_SIZE*x, TILE_SIZE*y) )
        pygame.display.flip()
    def getEvents(self):
        return pygame.event.get()
    def quit(self):
        pygame.quit()


class Region:
    """Someday, this might grow into the ability to have different
    regions with their own sets of rooms and their own image libraries."""
    def __init__(self):
        self.imageLibrary = ImageLibrary('drawntiles64')
