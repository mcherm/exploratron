import pygame
pygame.init()
from screenchanges import *
from players import thePlayerCatalog
from objects import defaultRegion, Dirt
from gamecomponents import Room


def makePlayer(id="0"):
    return thePlayerCatalog.getEntryById(id).getPlayer(defaultRegion)

def makeRoom(players=None):
    room = Room(
        [
            [Dirt(), Dirt()],
            [Dirt(), Dirt()],
        ]
    )
    for player in players:
        coordinates = (0, 1)
        player.setLocation(room, coordinates)
        room.cellAt(*coordinates).addThing(player)
    return room


def test_noConsoleText():
    player = makePlayer()
    screenChanges = ScreenChanges()
    assert screenChanges.getConsoleTextsForPlayer(player) == []

def test_addConsoleTextForPlayer():
    player = makePlayer()
    screenChanges = ScreenChanges()
    screenChanges.addConsoleTextForPlayer(player, "one")
    assert screenChanges.getConsoleTextsForPlayer(player) == ["one"]

def test_addConsoleTextsForPlayer():
    player = makePlayer()
    screenChanges = ScreenChanges()
    screenChanges.addConsoleTextForPlayer(player, "one")
    screenChanges.addConsoleTextForPlayer(player, "two")
    screenChanges.addConsoleTextForPlayer(player, "three")
    assert screenChanges.getConsoleTextsForPlayer(player) == ["one", "two", "three"]

def test_addConsoleTextForMultiplePlayers():
    p1 = makePlayer("0")
    p2 = makePlayer("1")
    screenChanges = ScreenChanges()
    screenChanges.addConsoleTextForPlayer(p1, "one")
    screenChanges.addConsoleTextForPlayer(p1, "two")
    screenChanges.addConsoleTextForPlayer(p2, "three")
    screenChanges.addConsoleTextForPlayer(p1, "four")
    screenChanges.addConsoleTextForPlayer(p2, "five")
    assert screenChanges.getConsoleTextsForPlayer(p1) == ["one", "two", "four"]
    assert screenChanges.getConsoleTextsForPlayer(p2) == ["three", "five"]

def test_addConsoleTextThenClearIt():
    player = makePlayer()
    screenChanges = ScreenChanges()
    screenChanges.addConsoleTextForPlayer(player, "one")
    assert screenChanges.getConsoleTextsForPlayer(player) == ["one"]
    screenChanges.clear()
    assert screenChanges.getConsoleTextsForPlayer(player) == []

def test_addConsoleTextForEmptyRoom():
    player = makePlayer()
    room = makeRoom([])
    screenChanges = ScreenChanges()
    screenChanges.addConsoleTextForRoom(room, "one")
    assert screenChanges.getConsoleTextsForPlayer(player) == []


def test_addConsoleTextForRoom():
    player = makePlayer()
    room = makeRoom([player])
    screenChanges = ScreenChanges()
    screenChanges.addConsoleTextForRoom(room, "one")
    assert screenChanges.getConsoleTextsForPlayer(player) == ["one"]

def test_addMessageForAllWithMixedTiming():
    p1 = makePlayer("0")
    p2 = makePlayer("1")
    p3 = makePlayer("2")
    screenChanges = ScreenChanges()
    screenChanges.addConsoleTextForPlayer(p1, "one")
    screenChanges.addConsoleTextForAll("two")
    screenChanges.addConsoleTextForPlayer(p2, "three")
    screenChanges.addConsoleTextForAll("four")
    assert screenChanges.getConsoleTextsForPlayer(p1) == ["one", "two", "four"]
    assert screenChanges.getConsoleTextsForPlayer(p2) == ["two", "three", "four"]
    assert screenChanges.getConsoleTextsForPlayer(p3) == ["two", "four"]
