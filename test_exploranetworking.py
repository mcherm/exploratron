#
# Unit tests for exploranetworking using the pytest library
#

from exploranetworking import *


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


