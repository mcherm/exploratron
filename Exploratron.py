#
# This contains the game currently known as "Exploratron". 
#

import pygame
import kindsofthing
from kindsofthing import *
from objects import *
import rooms
import time


# ========= Start Classes for Game =========

    


class World:
    """Represents the entire world."""
    def __init__(self):
        self.gameOver = False
        self.rooms = rooms.rooms
        self.mobiles = []
        # set up player
        self.player = Player(11,9)
        playerRoom = self.rooms[1]
        self.player.setLocation( playerRoom, (2,1) )
        playerRoom.cellAt(2,1).addThing(self.player)
    def addMobiles(self, newMobiles):
        """Call this to add some new mobiles to the list of active
        mobiles."""
        self.mobiles.extend(newMobiles)

        
class PlayerInputs:
    def __init__(self, events):
        self.events = events

        
# ========= End Classes for Game =========


# ========= Start Drawing Stuff =========

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
    def show(self, room, imageLibrary):
        self.screen.fill( (0,0,0) )
        for y in range(room.height):
            for x in range(room.width):
                cell = room.cellAt(x,y)
                for thing in cell.things:
                    image = imageLibrary.lookup( thing.tileId )
                    self.screen.blit( image, (TILE_SIZE*x, TILE_SIZE*y) )
        pygame.display.flip()
    def quit(self):
        pygame.quit()


class PygameInput:
    def __init__(self):
        pygame.event.set_allowed(None)
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
    def getEvents(self):
        return pygame.event.get()


# ========= End Drawing Stuff ==========

# ========= Start Functions for Game =========


def moveMobiles(world, currentTime):
    """This function will cause all of the mobiles to move one step,
    updating the world accordingly."""
    for mobile in world.mobiles:
        if currentTime >= mobile.whenItCanAct:
            mobile.takeOneStep(currentTime)
    

def getPlayerInputs(pygameInput):
    events = pygameInput.getEvents()
    return PlayerInputs(events)


def isNonActionEvent(event):
    """Retrns True if this is an event that can be processed when the
    player does not have an action, and False otherwise."""
    return event.type == pygame.QUIT
    
def isActionEvent(event):
    """Returns true if this is an event that can only be processed when
    the player has an action, and False otherwise."""
    return (event.type == pygame.KEYDOWN and
        event.key in (pygame.K_s, pygame.K_w, pygame.K_d, pygame.K_a))


def updateWorld(world, playerInputs):
    currentTime = int(time.perf_counter()*1000)
    events = playerInputs.events
    if events:
        # Non-Action Events
        for event in filter(isNonActionEvent, events):
            if event.type == pygame.QUIT:
                world.gameOver = True
    # Action Events
    if currentTime < world.player.whenItCanAct:
        # Player cannot act yet
        if (world.player.queuedEvent is None) and events:
            # Player does not have an event queued
            for event in filter(isActionEvent, events):
                world.player.queuedEvent = event
                break
    else:
        # Player can act now
        eventToActOn = world.player.queuedEvent
        # We used the value, so clear it
        world.player.queuedEvent = None
        if eventToActOn is None:
            # Set eventToActOn to the FIRST action event
            for event in filter(isActionEvent, events):
                eventToActOn = event
                break
        # Now we have set eventToActOn
        if eventToActOn is not None:
            if eventToActOn.type == pygame.KEYDOWN:
                if eventToActOn.key == pygame.K_s:
                    world.player.moveSouth()
                    world.player.whenItCanAct = currentTime + 500
                if eventToActOn.key == pygame.K_w:
                    world.player.moveNorth()
                    world.player.whenItCanAct = currentTime + 500
                if eventToActOn.key == pygame.K_d:
                    world.player.moveEast()
                    world.player.whenItCanAct = currentTime + 500
                if eventToActOn.key == pygame.K_a:
                    world.player.moveWest()
                    world.player.whenItCanAct = currentTime + 500
    # Move Mobiles
    moveMobiles(world, currentTime)
            
    


def renderWorld(player, display, imageLibrary):
    display.show(player.room, imageLibrary)



def mainLoop(world):
    display = PygameGridDisplay()
    imageLibrary = ImageLibrary()
    pygameInput = PygameInput()
    player = world.player
    while not world.gameOver:
        renderWorld(player, display, imageLibrary)
        playerInputs = getPlayerInputs(pygameInput)
        updateWorld(world, playerInputs)
    display.quit()

# ========= End Functions for Game =========

kindsofthing.world = World()
mainLoop(kindsofthing.world)
