#
# This file has code needed to create the nice UI used to
# view the inventory
#

import pygame
from images import TILE_SIZE

LIGHT_GREY = (120, 120, 120)
TRACK_COLOR = (0,0,0)
INVENTORY_MARGIN = 10  # distance in pixels from edge of screen to edge of showing the inventory
BORDER = 3  # distance in pixels around each item
AISLE_SIZE = TILE_SIZE // 2  # width of the aisle between columns of items
TRACK_WIDTH = 7


CROSSHAIR_SIZE = 32
HALF_CROSSHAIR_SIZE = CROSSHAIR_SIZE // 2

class Crosshair:
    def __init__(self):
        self.image = None
    def drawAt(self, surface, xy):
        """Draw the crosshair centered at the given xy = (x,y) location."""
        if self.image is None:
            self.image = pygame.image.load("./img/special/crosshair.png")
        x, y = xy
        surface.blit(self.image, (x - HALF_CROSSHAIR_SIZE, y - HALF_CROSSHAIR_SIZE))
crosshair = Crosshair()


def pairwise(iterable):
    """Returns the contents as a list of pairs (padding the last slot with None
    if there were an odd number).

    NOTE: If this were designed for reuse I would make it return an iterator
    instead of a list."""
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
            result.append((first, None))
            break
        result.append((first, second))
    return result



class InventoryView:
    """An instance of this class is part of the UI representing an active
    view of the inventory. In the initialization of the class it will read
    the inventory and decide how to lay it out; it will also maintain a
    crosshair position and draw to the screen as needed."""

    def __init__(self, inventory):
        """Passed an Inventory object with the current set of items to display."""
        self.itemsInBag = list(inventory)
        self.wornWeapon = inventory.getWieldedWeapon()
        if self.wornWeapon is not None:
            self.itemsInBag.remove(self.wornWeapon) # Do not show worn weapon in the bag
        self.itemsInBag.append(None) # add a blank space in the bag
        self.shouldExit = False
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
        itemPairs = itemPairs[:rowsThatCanFit]  # truncate to what can fit on the screen
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
        if self.wornWeapon is not None:
            wornWeaponImage = imageLibrary.lookupById(self.wornWeapon.tileId)
            surface.blit(wornWeaponImage, (self.wornItemsRegion.left + BORDER, self.wornItemsRegion.top + BORDER))

    def show(self, surface, imageLibrary):
        if not self.hasLaidOutScreen:
            self.layOutScreen(surface)
        self.showBag(surface, imageLibrary)
        self.showWornItems(surface, imageLibrary)
        self.showTrack(surface)
        crosshair.drawAt(surface, self.crosshairPixelPos())

    def moveCrosshairSouth(self):
        if self.crosshairPositionX == 0 and self.crosshairPositionY < len(self.itemPairs):
            self.crosshairPositionY += 1

    def moveCrosshairNorth(self):
        if self.crosshairPositionX == 0 and self.crosshairPositionY == 0:
            # exit the inventory view
            self.shouldExit = True
        if self.crosshairPositionX == 0 and self.crosshairPositionY > 0:
            self.crosshairPositionY -= 1

    def moveCrosshairEast(self):
        if self.crosshairPositionX < 1:
            self.crosshairPositionX += 1

    def moveCrosshairWest(self):
        if self.crosshairPositionX > -1:
            self.crosshairPositionX -= 1

    def takeAction(self, person):
        if self.crosshairPositionX == 0:
            pass # Do nothing if in the center
        elif self.crosshairPositionY == len(self.itemPairs):
            pass # Do nothing if in the worn items section
        else:
            # If on an item, drop it where we stand
            pair = self.itemPairs[self.crosshairPositionY]
            whichItem = 0 if self.crosshairPositionX < 0 else 1
            item = pair[whichItem]
            if item is not None:
                try:
                    person.inventory.removeItem(item) # take it out the inventory
                except ValueError:
                    # Must no longer be in the inventory. So do nothing
                    return
                person.placeItem(item)
                self.itemPairs[self.crosshairPositionY] = (
                    (None, pair[1]) if self.crosshairPositionX < 0 else (pair[0], None)
                )

