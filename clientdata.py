import copy


class ClientDataStructure:
    """Common parent class for some types which are intended to be passed around in the
    messages sent to the front-end."""
    def toJSON(self):
        raise NotImplementedError # subclasses should implement this

    @classmethod
    def fromJSON(cls):
        raise NotImplementedError # subclasses should implement this


class CellData(ClientDataStructure):
    """In JSON, a CellData is EITHER a number (representing the single tileId in that
    location) OR a list of numbers (representing the stack of tiles in that
    location)."""
    def __init__(self, tileIds):
        """Initialize a cell from a tuple of tileIds."""
        assert isinstance(tileIds, tuple)
        self._tileIds = tileIds

    def __eq__(self, other):
        return isinstance(other, CellData) and  self._tileIds == other._tileIds

    @classmethod
    def fromJSON(cls, json):
        """Initialize a cell from the corresponding JSON."""
        if isinstance(json, int):
            return cls(tileIds=(json,))
        elif isinstance(json, list):
            return cls(tileIds=tuple(json))
        else:
            raise TypeError("CellData must be an integer or list of integers.")

    def toJSON(self):
        """Return this Cell in JSON format."""
        if len(self._tileIds) == 1:
            return self._tileIds[0]
        else:
            return list(self._tileIds)

    def tileIds(self):
        """Returns an iterable of the items in this cell."""
        for x in self._tileIds:
            yield x


class GridData(ClientDataStructure):
    """A GridData represents the contents of a room. In JSON, a grid is a 2-D array
    (list of lists) of (the JSON representation of) cells."""
    def __init__(self, width, height, allCells):
        """Initialize a grid from width, height, and allCells."""
        self.width = width
        self.height = height
        self._allCells = allCells

    @classmethod
    def fromJSON(cls, json):
        """Initialize a grid from the corresponding JSON."""
        allCells = [] # array of all cells, indexed by [x + (y * width)]
        assert isinstance(json, list)
        height = len(json)
        assert height > 0   # otherwise width would be undefined
        width = len(json[0])
        for row in json:
            assert isinstance(row, list)
            assert len(row) == width
            allCells.extend(CellData.fromJSON(x) for x in row)
        return cls(width, height, allCells)

    def toJSON(self):
        """Return this Grid in JSON format."""
        return [[self.cellAt(x,y).toJSON() for x in range(self.width)] for y in range(self.height)]

    def cellAt(self, x, y):
        """Returns the CellData at the specified x,y location (which must be valid for this GridData)."""
        assert 0 <= x < self.width
        assert 0 <= y <= self.height
        return self._allCells[x + self.width * y]

    def _setCellAt(self, x, y, cellData):
        """Use only by GridChanges; this makes it mutable. Update one cell, replacing the contents."""
        assert 0 <= x < self.width
        assert 0 <= y <= self.height
        self._allCells[x + self.width * y] = cellData


class GridDataChange(ClientDataStructure):
    """This represents a set of changes that can be applied to an existing grid.
    In JSON, it is a list of three-element lists [x,y,cell] where x and y should
    be within the range of the grid it is to be applied to and cell is (the JSON
    representation of) a cell."""
    def __init__(self, changes):
        """Initialize a GridChange a list of (x,y,CellData) tuples."""
        self._changes = changes

    @classmethod
    def fromJSON(cls, json):
        """Initialize a GridChange from the corresponding JSON."""
        assert isinstance(json, list)
        return cls(changes=[(x, y, CellData.fromJSON(cellJSON)) for x, y, cellJSON in json])

    def toJSON(self):
        """Return this GridChange in JSON format."""
        return [[x, y, cellData.toJSON()] for x, y, cellData in self._changes]

    def changes(self):
        """Returns an iterator of (x, y, CellData) tuples."""
        return iter(self._changes)

    def applyToGrid(self, gridData):
        """When invoked, modifies the given grid by applying these changes. Will
        give an error if that doesn't work."""
        assert isinstance(gridData, GridData)
        for x, y, cellData in self.changes():
            gridData._setCellAt(x, y, cellData)


class VisibleData(ClientDataStructure):
    """This represents only the properties that are continuously displayed on the
    client side and sent every time they change. So it includes things like the
    current player's rendered stats, but not things like the current message or
    inventory which would be large and don't need to be sent every time."""
    def __init__(self, health, maxHealth, mana, maxMana):
        self.health = health
        self.maxHealth = maxHealth
        self.mana = mana
        self.maxMana = maxMana

    def __eq__(self, other):
        return isinstance(other, VisibleData) and self.__dict__ == other.__dict__

    @classmethod
    def fromJSON(cls, json):
        """Initialize a DisplayedPlayerData from the corresponding JSON."""
        return cls(**json)

    @classmethod
    def fromEnvironment(cls, player):
        """Initialize a DisplayedPlayerData from whatever sources are needed, which is
        currently just the player that is active on this connection."""
        return cls(
            health=player.stats.health,
            maxHealth=player.stats.maxHealth,
            mana=player.stats.mana,
            maxMana=player.stats.maxMana)

    def toJSON(self):
        """Return this DisplayedPlayerData in JSON format."""
        return copy.copy(self.__dict__)


class InventoryItemData(ClientDataStructure):
    """This represents a single item in an inventory. It is defined as:
    [uniqueId, tileId, featureCode]. (It would be more elegant to use a dict, but
    space might matter so we'll use the list instead.)"""
    def __init__(self, uniqueId, tileId, featureCode):
        self.uniqueId = uniqueId
        self.tileId = tileId
        self.featureCode = featureCode

    def __eq__(self, other):
        return isinstance(other, InventoryItemData) and  self.uniqueId == other.uniqueId

    @classmethod
    def fromJSON(cls, json):
        """Initialize from the corresponding JSON."""
        assert isinstance(json, list)
        assert len(json) == 3
        return cls(*json)

    @classmethod
    def fromItem(cls, item):
        """Initialize an InventoryItemData from an actual Item."""
        return cls(
            uniqueId=item.uniqueId(),
            tileId=item.tileId,
            featureCode=item.featureCode())

    def toJSON(self):
        """Return this in JSON format."""
        return [self.uniqueId, self.tileId, self.featureCode]

    def isWeapon(self):
        return self.featureCode == "W"

    def isWand(self):
        return self.featureCode == "S"


class InventoryData(ClientDataStructure):
    """This represents a snapshot of the inventory."""
    def __init__(self, items, wieldedWeaponId, wieldedWandId):
        self.items = items # a list of InventoryItemData objects
        self.wieldedWeaponId = wieldedWeaponId
        self.wieldedWandId = wieldedWandId

    @classmethod
    def fromJSON(cls, json):
        """Initialize from the corresponding JSON."""
        items = [InventoryItemData.fromJSON(x) for x in json["items"]]
        wieldedWeaponId = json["wieldedWeaponId"]
        wieldedWandId = json["wieldedWandId"]
        return cls(items, wieldedWeaponId, wieldedWandId)

    @classmethod
    def fromInventory(cls, inventory):
        """Initialize from an Inventory."""
        items = [InventoryItemData.fromItem(item) for item in inventory.items]
        wieldedWeapon = inventory.getWieldedWeapon()
        wieldedWeaponId = None if wieldedWeapon is None else wieldedWeapon.uniqueId()
        wieldedWand = inventory.getWieldedWand()
        wieldedWandId = None if wieldedWand is None else wieldedWand.uniqueId()
        return cls(items, wieldedWeaponId, wieldedWandId)

    def toJSON(self):
        """Return this in JSON format."""
        return {
            "items": [x.toJSON() for x in self.items],
            "wieldedWeaponId": self.wieldedWeaponId,
            "wieldedWandId": self.wieldedWandId,
        }
