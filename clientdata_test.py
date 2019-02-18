#
# Unit tests for clientdata using the pytest library
#

from clientdata import *
from kindsofthing import Item


def test_CellData_Singleton():
    cellData = CellData.fromJSON(6)
    assert cellData.toJSON() == 6


def test_CellData_List():
    cellData = CellData.fromJSON([6,3,27])
    assert cellData.toJSON() == [6,3,27]


def test_CellData_simplestForm():
    assert CellData.fromJSON([2]).toJSON() == 2


def test_CellData_eq():
    cellDataA = CellData.fromJSON(6)
    cellDataB = CellData.fromJSON(6)
    cellDataC = CellData.fromJSON([5,13])
    cellDataD = CellData.fromJSON([5,13])
    assert cellDataA == cellDataB
    assert cellDataC == cellDataD
    assert cellDataA != cellDataC


def test_GridData_1():
    jsonData = [[4,4,4], [[4,2],4,[4,7,8]]]
    gridData = GridData.fromJSON(jsonData)
    assert gridData.height == 2
    assert gridData.width == 3
    for y, row in enumerate(jsonData):
        for x, item in enumerate(row):
            assert(gridData.cellAt(x,y).toJSON() == item)


def test_GridChanges_1():
    jsonData = [[0,0,2], [1,2,[4,5]]]
    assert CellData.fromJSON(jsonData).toJSON() == jsonData


def test_GridChange_Empty():
    jsonData = []
    assert GridDataChange.fromJSON(jsonData).toJSON() == jsonData


def test_GridChange_changes():
    gridDataChange = GridDataChange.fromJSON([[0, 0, 1], [1, 2, [8, 5]]])
    changeList = list(gridDataChange.changes())
    assert changeList == [
        (0,0,CellData.fromJSON(1)),
        (1,2,CellData.fromJSON([8,5]))
    ]


def test_GridChange_Apply():
    grid = GridData.fromJSON([[4,4,4], [4,4,4], [4,4,4], [4,4,4]])
    assert list(grid.cellAt(0,0).tileIds()) == [4]
    gridDataChange = GridDataChange.fromJSON([[0, 0, 1], [1, 2, [8, 5]]])
    gridDataChange.applyToGrid(grid)
    assert list(grid.cellAt(0,0).tileIds()) == [1]
    assert list(grid.cellAt(1,2).tileIds()) == [8,5]


def test_VisibleData_1():
    jsonData = {"health": 10, "maxHealth": 10, "mana": 4, "maxMana": 8}
    assert VisibleData.fromJSON(jsonData).toJSON() == jsonData


def test_VisibleData_eq():
    jsonDataA = {"health": 10, "maxHealth": 10, "mana": 4, "maxMana": 8}
    jsonDataB = {"health": 10, "maxHealth": 25, "mana": 4, "maxMana": 8}
    visibleDataA1 = VisibleData.fromJSON(jsonDataA)
    visibleDataA2 = VisibleData.fromJSON(jsonDataA)
    visibleDataB1 = VisibleData.fromJSON(jsonDataB)
    assert visibleDataA1 == visibleDataA2
    assert visibleDataA1 != visibleDataB1


def test_InventoryItemData_1():
    jsonData = [4392386512, 6, "N"]
    inventoryItemData = InventoryItemData.fromJSON(jsonData)
    assert inventoryItemData.uniqueId == 4392386512
    assert inventoryItemData.tileId == 6
    assert inventoryItemData.featureCode == "N"
    assert inventoryItemData.toJSON() == jsonData


def test_InventoryItemData_eq():
    jsonDataA = [4392386512, 6, "N"]
    jsonDataB = [4392479488, 6, "N"]
    inventoryItemDataA1 = InventoryItemData.fromJSON(jsonDataA)
    inventoryItemDataA2 = InventoryItemData.fromJSON(jsonDataA)
    inventoryItemDataB1 = InventoryItemData.fromJSON(jsonDataB)
    assert inventoryItemDataA1 == inventoryItemDataA2
    assert inventoryItemDataA1 != inventoryItemDataB1


def test_InventoryItemData_weapon():
    def ii(code):
        return InventoryItemData.fromJSON([4392386512, 6, code])
    assert not ii("N").isWeapon()
    assert ii("W").isWeapon()
    assert not ii("S").isWeapon()


def test_InventoryItemData_wand():
    def ii(code):
        return InventoryItemData.fromJSON([4392386512, 6, code])
    assert not ii("N").isWand()
    assert not ii("W").isWand()
    assert ii("S").isWand()


def test_InventoryData_1():
    jsonData = {"items": [[4392479488, 3, "N"], [4392386512, 4, "S"]], "wieldedWeaponId": None, "wieldedWandId": 4392386512}
    inventoryData = InventoryData.fromJSON(jsonData)
    assert inventoryData.toJSON() == jsonData
