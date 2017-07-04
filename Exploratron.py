#
# This contains the game currently known as "Exploratron". 
#

import pygame
import kindsofthing
from kindsofthing import *
from objects import *
from images import ImageLibrary, TILE_SIZE, PygameGridDisplay
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






# ========= End Drawing Stuff ==========

# ========= Start Functions for Game =========


def moveMobiles(world, currentTime):
    """This function will cause all of the mobiles to move one step,
    updating the world accordingly."""
    for mobile in world.mobiles:
        if currentTime >= mobile.whenItCanAct:
            mobile.takeOneStep(currentTime)
    


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
    # Check for Death
    handleDeath(world)
            

def handleDeath(world):
    for mobile in world.mobiles:
        if mobile.isDead:
            x, y = mobile.position
            cell = mobile.room.cellAt(x, y)
            cell.removeThing(mobile)
            world.mobiles.remove(mobile)
    if world.player.isDead:
        x, y = world.player.position
        cell = world.player.room.cellAt(x, y)
        cell.removeThing(world.player)
        world.gameOver = True


def renderWorld(player, display, imageLibrary):
    display.show(player.room, imageLibrary)



def mainLoop(world):
    display = PygameGridDisplay()
    imageLibrary = ImageLibrary()
    player = world.player
    while not world.gameOver:
        renderWorld(player, display, imageLibrary)
        playerInputs = PlayerInputs(display.getEvents())
        updateWorld(world, playerInputs)
    display.quit()



# ========= End Functions for Game =========

kindsofthing.world = World()
mainLoop(kindsofthing.world)
