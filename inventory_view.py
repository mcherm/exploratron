#
# This file has code needed to create the nice UI used to
# view the inventory
#

import pygame
from images import TILE_SIZE
from kindsofthing import Weapon, Wand


LIGHT_GREY = (120, 120, 120)
TRACK_COLOR = (0,0,0)
INVENTORY_MARGIN = 10  # distance in pixels from edge of screen to edge of showing the inventory
BORDER = 3  # distance in pixels around each item
AISLE_SIZE = TILE_SIZE // 2  # width of the aisle between columns of items
TRACK_WIDTH = 7


CROSSHAIR_SIZE = 32
HALF_CROSSHAIR_SIZE = CROSSHAIR_SIZE // 2

class Crosshair:
    def __init__(self, specialImageName):
        self.specialImageName = specialImageName
        self.image = None
    def drawAt(self, surface, xy):
        """Draw the crosshair centered at the given xy = (x,y) location."""
        if self.image is None:
            self.image = pygame.image.load(f"./img/special/{self.specialImageName}.png")
        x, y = xy
        surface.blit(self.image, (x - HALF_CROSSHAIR_SIZE, y - HALF_CROSSHAIR_SIZE))
pointer = Crosshair("crosshair")
hand = Crosshair("hand")


def pairwise(iterable):
    """Returns the contents as a list of 2-element lists (padding the last slot
    with None if there were an odd number).

    NOTE: If this were designed for reuse I would make it return an iterator
    instead of a list and tuples instead of lists."""
    result = []
    it = iter(iterable)
    while True:
        try:
            first = next(it)
        except StopIteration:
            break
        try:
            second = next(it)
        except StopIteration:
            result.append([first, None])
            break
        result.append([first, second])
    return result



class InventoryView:
    """An instance of this class is part of the UI representing an active
    view of the inventory. In the initialization of the class it will read
    the inventory and decide how to lay it out; it will also maintain a
    crosshair position and draw to the screen as needed."""

    def __init__(self, player):
        """Passed a Player whose Inventory we will display, and who will drop any items
        carried off of the screen."""
        self.player = player
        self.itemsInBag = list(player.inventory)
        self.wieldedWeapon = player.inventory.getWieldedWeapon()
        self.wieldedWand = player.inventory.getWieldedWand()
        if self.wieldedWeapon is not None:
            self.itemsInBag.remove(self.wieldedWeapon) # Do not show wielded weapon in the bag
        if self.wieldedWand is not None:
            self.itemsInBag.remove(self.wieldedWand) # Do not show wielded wand in the bag
        self.itemsInBag.append(None) # add a blank space in the bag
        self.shouldExit = False
        self.itemBeingMoved = None
        self.hasLaidOutScreen = False
        # Other fields self.itemPairs, self.bagRegion, self.crosshairX, self.crosshairY
        # are set during the layOutScreen() method

    def layOutScreen(self, surface):
        """This is called only the first time that we try drawing it; it decides
        how everything is laid out. The layout cannot happen inside __init__()
        because it depends on the surface."""
        self.hasLaidOutScreen = True
        screenWidth, screenHeight = surface.get_size()
        rowsThatCanFit = (screenHeight - (2 * INVENTORY_MARGIN) - BORDER) // (TILE_SIZE + BORDER)

        itemPairs = pairwise(self.itemsInBag)
        itemPairs = itemPairs[:rowsThatCanFit]  # truncate to what can fit on the screen FIXME: Shouldn't do this
        self.itemPairs = itemPairs
        rows = len(itemPairs)

        # Determine the bag region
        bagRegion = pygame.Rect(
            0, 0,
            BORDER + TILE_SIZE + AISLE_SIZE + TILE_SIZE + BORDER,
            BORDER + rows * (TILE_SIZE + BORDER)
        )
        bagRegion.centerx = screenWidth / 2
        bagRegion.move_ip(0, INVENTORY_MARGIN)
        self.bagRegion = bagRegion

        # determine the bridgeRegion and wornItemsRegion
        bridgeRegion = pygame.Rect(0, bagRegion.bottom, AISLE_SIZE, AISLE_SIZE)
        bridgeRegion.centerx = bagRegion.centerx
        self.bridgeRegion = bridgeRegion
        self.wornItemsRegion = pygame.Rect(
            self.bagRegion.left,
            self.bagRegion.bottom + AISLE_SIZE,
            self.bagRegion.width,
            TILE_SIZE + 2 * BORDER
        )

        # location in pixels where crosshair goes if its position is (0,0)
        self.crosshairBaseX = bagRegion.centerx
        self.crosshairBaseY = bagRegion.top + BORDER + (TILE_SIZE // 2)
        self.crosshairPositionX = 0
        self.crosshairPositionY = 0

    def crosshairPixelPos(self):
        """Returns (x,y) position in pixels for the crosshair."""
        xPos = self.crosshairBaseX + self.crosshairPositionX * (TILE_SIZE + AISLE_SIZE) // 2
        if self.crosshairPositionY == len(self.itemPairs):
            # In the worn items section
            yPos = self.wornItemsRegion.top + BORDER + TILE_SIZE // 2
        else:
            yPos = self.crosshairBaseY + self.crosshairPositionY * (TILE_SIZE + BORDER)
        return xPos, yPos

    def showTrack(self, surface):
        """Draws the lines that show where the cursor can be moved."""
        pygame.draw.line(
            surface,
            TRACK_COLOR,
            (self.bagRegion.centerx, self.bagRegion.top),
            (self.wornItemsRegion.centerx, self.wornItemsRegion.bottom - BORDER - TILE_SIZE//2),
            TRACK_WIDTH
        )
        # Inventory section
        for i in range(0, len(self.itemPairs)):
            pygame.draw.line(
                surface,
                TRACK_COLOR,
                (self.crosshairBaseX - AISLE_SIZE//2, self.crosshairBaseY + i * (TILE_SIZE + BORDER)),
                (self.crosshairBaseX + AISLE_SIZE//2, self.crosshairBaseY + i * (TILE_SIZE + BORDER)),
                TRACK_WIDTH
            )
        # Worn Items Section
        pygame.draw.line(
            surface,
            TRACK_COLOR,
            (self.wornItemsRegion.centerx - AISLE_SIZE//2, self.wornItemsRegion.centery),
            (self.wornItemsRegion.centerx + AISLE_SIZE//2, self.wornItemsRegion.centery),
            TRACK_WIDTH
        )

    def showBag(self, surface, imageLibrary):
        surface.fill(LIGHT_GREY, self.bagRegion)
        leftItemXPos = self.bagRegion.left + BORDER
        rightItemXPos = leftItemXPos + TILE_SIZE + AISLE_SIZE
        for rowNum, (leftItem, rightItem) in enumerate(self.itemPairs):
            itemYPos = self.bagRegion.top + BORDER + rowNum * (TILE_SIZE + BORDER)
            if leftItem is not None:
                leftImage = imageLibrary.lookupById(leftItem.tileId)
                surface.blit(leftImage, (leftItemXPos, itemYPos))
            if rightItem is not None:
                rightImage = imageLibrary.lookupById(rightItem.tileId)
                surface.blit(rightImage, (rightItemXPos, itemYPos))

    def showWornItems(self, surface, imageLibrary):
        surface.fill(LIGHT_GREY, self.bridgeRegion)
        surface.fill(LIGHT_GREY, self.wornItemsRegion)
        if self.wieldedWeapon is not None:
            wieldedWeaponImage = imageLibrary.lookupById(self.wieldedWeapon.tileId)
            surface.blit(wieldedWeaponImage,
                         (self.wornItemsRegion.left + BORDER,
                          self.wornItemsRegion.top + BORDER))
        if self.wieldedWand is not None:
            wieldedWandImage = imageLibrary.lookupById(self.wieldedWand.tileId)
            surface.blit(wieldedWandImage,
                         (self.wornItemsRegion.right - (TILE_SIZE + BORDER),
                          self.wornItemsRegion.top + BORDER))


    def show(self, surface, imageLibrary):
        if not self.hasLaidOutScreen:
            self.layOutScreen(surface)
        self.showBag(surface, imageLibrary)
        self.showWornItems(surface, imageLibrary)
        self.showTrack(surface)
        if self.itemBeingMoved is None:
            crosshair = pointer
        else:
            itemImage = imageLibrary.lookupById(self.itemBeingMoved.tileId)
            x,y = self.crosshairPixelPos()
            x -= TILE_SIZE // 2
            y -= TILE_SIZE // 2
            surface.blit(itemImage, (x,y))
            crosshair = hand
        crosshair.drawAt(surface, self.crosshairPixelPos())

    def moveCrosshairSouth(self):
        if self.crosshairPositionX == 0 and self.crosshairPositionY < len(self.itemPairs):
            self.crosshairPositionY += 1

    def moveCrosshairNorth(self):
        if self.crosshairPositionX == 0 and self.crosshairPositionY == 0:
            # exit the inventory view
            self.shouldExit = True
            if self.itemBeingMoved is not None:
                self.dropItem(self.itemBeingMoved)
        if self.crosshairPositionX == 0 and self.crosshairPositionY > 0:
            self.crosshairPositionY -= 1

    def moveCrosshairEast(self):
        if self.itemBeingMoved is None:
            if self.crosshairPositionX < 1:
                self.crosshairPositionX += 1
        else:
            if self.crosshairPositionX == -1:
                self.crosshairPositionX += 1
            elif self.crosshairPositionX == 0:
                if self.crosshairPositionY == len(self.itemPairs):
                    if self.wieldedWand is None and isinstance(self.itemBeingMoved, Wand):
                        self.crosshairPositionX += 1
                else:
                    if self.itemPairs[self.crosshairPositionY][1] is None:
                        self.crosshairPositionX += 1
                    else:
                        pass # Cannot put into a full slot
            elif self.crosshairPositionX == 1:
                pass # can't move right from there
            else:
                assert False # x position should be -1, 0, or 1!

    def moveCrosshairWest(self):
        if self.itemBeingMoved is None:
            if self.crosshairPositionX > -1:
                self.crosshairPositionX -= 1
        else:
            if self.crosshairPositionX == 1:
                self.crosshairPositionX -= 1
            elif self.crosshairPositionX == 0:
                if self.crosshairPositionY == len(self.itemPairs):
                    if self.wieldedWeapon is None and isinstance(self.itemBeingMoved, Weapon):
                        self.crosshairPositionX -= 1
                else:
                    if self.itemPairs[self.crosshairPositionY][0] is None:
                        self.crosshairPositionX -= 1
                    else:
                        pass # Cannot put into a full slot
            elif self.crosshairPositionX == -1:
                pass # can't move left from there
            else:
                assert False # x position should be -1, 0, or 1!

    def takeAction(self):
        if self.itemBeingMoved is None:
            # Picking an item!
            if self.crosshairPositionX == 0:
                pass # Do nothing if in the center
            elif self.crosshairPositionY == len(self.itemPairs):
                if self.crosshairPositionX == -1 and self.wieldedWeapon is not None:
                    self.itemBeingMoved = self.wieldedWeapon
                    self.wieldedWeapon = None
                    self.wieldWeapon(None) # Immediately mark it not worn
                    self.crosshairPositionX = 0 # Pop back to the center
                elif self.crosshairPositionX == 1 and self.wieldedWand is not None:
                    self.itemBeingMoved = self.wieldedWand
                    self.wieldedWand = None
                    self.wieldWand(None) # Immediately mark it as not worn
                    self.crosshairPositionX = 0 # Pop back to the center
                else:
                    pass # Do nothing for other positions
            else:
                # If on an item, start moving it around
                pair = self.itemPairs[self.crosshairPositionY]
                whichItem = 0 if self.crosshairPositionX < 0 else 1
                item = pair[whichItem]
                if item is not None:
                    self.itemBeingMoved = item
                    pair[whichItem] = None
                    self.crosshairPositionX = 0 # Pop back to the center
        else:
            # Moving an item!
            if self.crosshairPositionX == 0:
                pass # Do nothing if in the center
            elif self.crosshairPositionY == len(self.itemPairs):
                if self.crosshairPositionX == -1 and self.wieldedWeapon is None and isinstance(self.itemBeingMoved, Weapon):
                    self.wieldedWeapon = self.itemBeingMoved
                    self.itemBeingMoved = None
                    self.wieldWeapon(self.wieldedWeapon)
                    self.crosshairPositionX = 0 # Pop back to the center
                if self.crosshairPositionX == 1 and self.wieldedWand is None and isinstance(self.itemBeingMoved, Wand):
                    self.wieldedWand = self.itemBeingMoved
                    self.itemBeingMoved = None
                    self.wieldWand(self.wieldedWand)
                    self.crosshairPositionX = 0 # Pop back to the center
                else:
                    pass # do nothing
            else:
                # In the bag
                pair = self.itemPairs[self.crosshairPositionY]
                whichItem = 0 if self.crosshairPositionX < 0 else 1
                if pair[whichItem] is None:
                    pair[whichItem] = self.itemBeingMoved
                    self.itemBeingMoved = None
                    self.crosshairPositionX = 0 # Pop back to the center
                else:
                    # Already an item in this location. Do nothing
                    pass

    def dropItem(self, item):
        """Attempt to drop an item currently in the inventory. If the item actually turns
        out NOT to be in the inventory at this moment, this will do nothing."""
        if not self.player.isDead:
            try:
                self.player.inventory.removeItem(item)  # take it out the inventory
            except ValueError:
                # Must no longer be in the inventory. So do nothing
                return
            self.player.placeItem(item)

    def wieldWeapon(self, item):
        """If item is None, stops wielding the current weapon. If item is anything
        else, try to start wielding it as a Weapon. If for some reason this doesn't
        work (perhaps the inventory has changed since the InventoryView launched),
        then this does nothing."""
        if not self.player.isDead:
            try:
                self.player.inventory.wieldWeapon(item)
            except ValueError:
                # Must no longer be wielded. So do nothing
                return

    def wieldWand(self, item):
        """If item is None, stops wielding the current wand. If item is anything
        else, try to start wielding it as a Wand. If for some reason this doesn't
        work (perhaps the inventory has changed since the InventoryView launched),
        then this does nothing."""
        if not self.player.isDead:
            try:
                self.player.inventory.wieldWand(item)
            except ValueError:
                # Must no longer be wielded. So do nothing
                return

