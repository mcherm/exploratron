#
# A class for keeping track of what has changed on the screen during a
# particular update cycle, so we can send a minimized set of updates.
#

from collections import defaultdict
from infotext import InfoText
from players import Player


class SetOfEverything:
    """Sort of like a set, but it ignores all add() calls and has nothing in it."""
    def add(self, x):
        pass


class ScreenChanges:
    def __init__(self):
        self.changesByRoom = defaultdict(set) # map of room -> set of (x,y) pairs
        self.playerRoomSwitches = {} # map of player -> (oldRoom,newRoom)
        self.soundsToPlayByRoom = defaultdict(list) # map of room -> list of soundIds
        self.newInfoTexts = defaultdict(list) # map of player -> list of InfoTexts
        self.consoleTextsForAll = list()  # list of messages for any player not a key in playerConsoleTexts
        self.playerConsoleTexts = defaultdict(self.consoleTextsForAll.copy) # map of player -> list of strings
    def clear(self):
        """Calling this clears out the full list of changes."""
        self.changesByRoom.clear()
        self.playerRoomSwitches.clear()
        self.soundsToPlayByRoom.clear()
        self.newInfoTexts.clear()
        self.consoleTextsForAll.clear()
        self.playerConsoleTexts.clear()
    def changeCell(self, room, x, y):
        """Calling this adds a change to one cell of one room."""
        self.changesByRoom[room].add((x,y))
    def changeTwoCells(self, room, x1, y1, x2, y2):
        """Convenience method to change TWO cells in a room at once."""
        roomChangeSet = self.changesByRoom[room]
        roomChangeSet.add( (x1,y1) )
        roomChangeSet.add( (x2,y2) )
    def generalRoomChanges(self, room):
        """Call this when various changes may have been made in a room."""
        self.changesByRoom[room] = SetOfEverything()
    def roomPlaySound(self, room, soundId):
        """Call this when a sound should be played."""
        self.soundsToPlayByRoom[room].append(soundId)
    def playerSwitchedRooms(self, player, oldRoom, newRoom):
        """Call this when a player changes to a new room. If we want a
        player to be able to change rooms more than once per time that
        clear() is called, then the design will need to be changed."""
        assert player not in self.playerRoomSwitches
        self.playerRoomSwitches[player] = (oldRoom, newRoom)
    def getRoomSwitches(self, player):
        """Returns (oldRoom, newRoom) if the given player has switched
        rooms since clear() was last called; otherwise returns None."""
        return self.playerRoomSwitches.get(player)
    def getRoomChangeSet(self, room):
        """Returns either a SetOfEverything (if the room has changed
        drastically) or a set containing (x,y) pairs for the locations
        in the room that have changed since clear() was called."""
        return self.changesByRoom[room]
    def getRoomSounds(self, room):
        """Returns a list of new sounds that should begin playing in the given
        room starting with this set of ScreenChanges."""
        return self.soundsToPlayByRoom[room]
    def showInfoText(self, player, infoText):
        """Begins displaying the given InfoText in the UI."""
        assert isinstance(player, Player)
        assert isinstance(infoText, InfoText)
        self.newInfoTexts[player].append(infoText)
    def getNewInfoTexts(self, player):
        """Returns a list of new infoTexts to display (in order) for the given player."""
        assert isinstance(player, Player)
        return self.newInfoTexts[player]
    def addConsoleTextForPlayer(self, player, text):
        """Adds a new message to the console of the given player."""
        assert isinstance(player, Player)
        self.playerConsoleTexts[player].append(text)
    def addConsoleTextForRoom(self, room, text):
        """Adds a new message to the console of all players in a room."""
        for player in room.getPlayers():
            self.playerConsoleTexts[player].append(text)
    def addConsoleTextForAll(self, text):
        """Adds a new message to the console of all players."""
        for player in self.playerConsoleTexts:
            self.playerConsoleTexts[player].append(text)
        self.consoleTextsForAll.append(text)
    def getConsoleTextsForPlayer(self, player):
        """Returns a list of new console text strings (in order) for the given player."""
        return self.playerConsoleTexts[player]
    def printThemOut(self):
        """Used only for debugging, this dumps to the screen the whole
        list of changes."""
        if self.changesByRoom:
            print("Screen Changes:")
            for room, roomChangeSet in self.changesByRoom.items():
                roomChangeSet = self.changesByRoom[room]
                if isinstance(roomChangeSet, SetOfEverything):
                    changeMessage = "everything"
                else:
                    changeMessage = ' + '.join(str(x) for x in roomChangeSet)
                print(f"  Room {room} has changed {changeMessage}.")
        if self.soundsToPlayByRoom:
            for room, roomSounds in self.soundsToPlayByRoom.items():
                print(f"  Room {room} should play sounds {roomSounds}.")


