
import pygame

TILE_SIZE = 64


class ImageLibrary:
    def __init__(self):
        rootDir = './img'
        names = [
            'drawntiles64/dirt-1',
            'drawntiles64/dirt-1',
            'drawntiles64/dirt-1',
            'drawntiles64/dirt-1',
            'drawntiles64/dirt-1',
            'drawntiles64/stairs-down',
            'drawntiles64/chest2',
            'drawntiles64/wall-1',
            'drawntiles64/doorway-1',
            'drawntiles64/chest2',
            'drawntiles64/chest2',
            'drawntiles64/adventurer-1-boy',
            'drawntiles64/angry-bee',
            'drawntiles64/mouseman',
            'drawntiles64/green-snake',
          ]
        self.imageById = {}
        for imgnum, name in enumerate(names):
            self.imageById[imgnum] = pygame.image.load(
                f'{rootDir}/{name}.png')
    def lookup(self, imgnum):
        return self.imageById[imgnum]

    
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
                    image = imageLibrary.lookup( thing.tileId )
                    self.screen.blit( image, (TILE_SIZE*x, TILE_SIZE*y) )
        pygame.display.flip()
    def getEvents(self):
        return pygame.event.get()
    def quit(self):
        pygame.quit()

