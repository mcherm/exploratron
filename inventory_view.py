#
# This file has code needed to create the nice UI used to
# view the inventory
#

import pygame
from images import TILE_SIZE

LIGHT_GREY = (120, 120, 120)
INVENTORY_MARGIN = 10  # distance in pixels from edge of screen to edge of showing the inventory
BORDER = 3  # distance in pixels around each item
AISLE_SIZE = TILE_SIZE // 2  # width of the aisle between columns of items


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
        self.inventory = inventory
        self.hasLaidOutScreen = False
        # Other fields self.itemPairs, self.inventoryRegion, self.crosshairX, self.crosshairY
        # are set during the layOutScreen() method

    def layOutScreen(self, surface):
        """This is called only the first time that we try drawing it; it decides
        how everything is laid out. The layout cannot happen inside __init__()
        because it depends on the surface."""
        self.hasLaidOutScreen = True
        screenWidth, screenHeight = surface.get_size()
        rowsThatCanFit = (screenHeight - (2 * INVENTORY_MARGIN) - BORDER) // (TILE_SIZE + BORDER)

        itemPairs = pairwise(self.inventory)
        itemPairs = itemPairs[:rowsThatCanFit]  # truncate to what can fit on the screen
        self.itemPairs = itemPairs
        rows = len(itemPairs)

        inventoryRegion = pygame.Rect(
            0, 0,
            BORDER + TILE_SIZE + AISLE_SIZE + TILE_SIZE + BORDER,
            BORDER + rows * (TILE_SIZE + BORDER)
        )
        inventoryRegion.centerx = screenWidth / 2
        inventoryRegion.move_ip(0, INVENTORY_MARGIN)
        self.inventoryRegion = inventoryRegion
        self.crosshairX = inventoryRegion.centerx
        self.crosshairY = inventoryRegion.top + BORDER + (TILE_SIZE // 2)

    def show(self, surface, imageLibrary):
        if not self.hasLaidOutScreen:
            self.layOutScreen(surface)
        surface.fill(LIGHT_GREY, self.inventoryRegion)
        leftItemXPos = self.inventoryRegion.left + BORDER
        rightItemXPos = leftItemXPos + TILE_SIZE + AISLE_SIZE
        for rowNum, (leftItem, rightItem) in enumerate(self.itemPairs):
            itemYPos = self.inventoryRegion.top + BORDER + rowNum * (TILE_SIZE + BORDER)
            leftImage = imageLibrary.lookupById(leftItem.tileId)
            surface.blit(leftImage, (leftItemXPos, itemYPos))
            if rightItem is not None:
                rightImage = imageLibrary.lookupById(rightItem.tileId)
                surface.blit(rightImage, (rightItemXPos, itemYPos))
        crosshair.drawAt(surface, (self.crosshairX, self.crosshairY))

    def moveCrosshairSouth(self):
        self.crosshairY = self.crosshairY + TILE_SIZE + BORDER

    def moveCrosshairNorth(self):
        pass

    def moveCrosshairEast(self):
        pass

    def moveCrosshairWest(self):
        pass
