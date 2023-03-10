import pygame


class KeyCode:
    GO_UP = 1
    GO_DOWN = 2
    GO_LEFT = 3
    GO_RIGHT = 4
    PICK_UP = 5
    CAST = 6
    TOGGLE_INVENTORY = 7
    MOVE_UI_UP = 8
    MOVE_UI_DOWN = 9
    MOVE_UI_LEFT = 10
    MOVE_UI_RIGHT = 11
    UI_ACTION = 12

    

pygameKeyToKeyCode = {
    pygame.K_w: KeyCode.GO_UP,
    pygame.K_s: KeyCode.GO_DOWN,
    pygame.K_a: KeyCode.GO_LEFT,
    pygame.K_d: KeyCode.GO_RIGHT,
    pygame.K_UP: KeyCode.MOVE_UI_UP,
    pygame.K_DOWN: KeyCode.MOVE_UI_DOWN,
    pygame.K_LEFT: KeyCode.MOVE_UI_LEFT,
    pygame.K_RIGHT: KeyCode.MOVE_UI_RIGHT,
    pygame.K_SLASH: KeyCode.UI_ACTION,
    pygame.K_q: KeyCode.PICK_UP,
    pygame.K_e: KeyCode.CAST,
    pygame.K_i: KeyCode.TOGGLE_INVENTORY,
}

keyCodeToIsAction = {
    KeyCode.GO_UP: True,
    KeyCode.GO_DOWN: True,
    KeyCode.GO_LEFT: True,
    KeyCode.GO_RIGHT: True,
    KeyCode.PICK_UP: True,
    KeyCode.CAST: True,
    KeyCode.TOGGLE_INVENTORY: False,
    KeyCode.MOVE_UI_UP: False,
    KeyCode.MOVE_UI_DOWN: False,
    KeyCode.MOVE_UI_LEFT: False,
    KeyCode.MOVE_UI_RIGHT: False,
    KeyCode.UI_ACTION: False,
}


class Event:
    """Parent class for all events."""
    def isActionEvent(self):
        """Returns True if this event can only be processed when the player
        has an action and False otherwise."""
        return False

class QuitGameEvent(Event):
    """An event for when the game is going to exit (on the server)."""
    pass

class NewPlayerAddedEvent(Event):
    """An event for when it is discovered that a new player needs to be
    added at the next update stage."""
    def __init__(self, playerCatalogEntry, clientConnection):
        self.playerCatalogEntry = playerCatalogEntry
        self.clientConnection = clientConnection

class PlayerEvent(Event):
    """Any event that affects a specific player."""
    def __init__(self, playerId):
        self.playerId = playerId

class KeyPressedEvent(PlayerEvent):
    """An event where a key was pressed on the controls for a player."""
    def __init__(self, playerId, keyCode):
        super().__init__(playerId)
        self.keyCode = keyCode
    def isActionEvent(self):
        return keyCodeToIsAction[self.keyCode]

class ItemDroppedEvent(PlayerEvent):
    def __init__(self, playerId, itemUniqueId):
        super().__init__(playerId)
        self.itemUniqueId = itemUniqueId

class EquipItemEvent(PlayerEvent):
    def __init__(self, playerId, equipmentTypeCode, itemUniqueId):
        super().__init__(playerId)
        self.equipmentTypeCode = equipmentTypeCode
        self.itemUniqueId = itemUniqueId

class ClientConnectEvent(PlayerEvent):
    """An event where a new client is connecting to a specific player."""
    def __init__(self, playerId):
        super().__init__(playerId)

class ClientDisconnectEvent(PlayerEvent):
    """An event where a client DISCONNECTS from a specific player."""
    def __init__(self, playerId):
        super().__init__(playerId)


class EventList:
    """This class maintains a list of events."""
    def __init__(self):
        self.actionEvents = {} # map playerId to just ONE event (the first one we got)
        self.nonActionEvents = [] # List of all non-action events
    def __str__(self):
        return f'<EventList with {len(self.actionEvents)+len(self.nonActionEvents)} events>'
    def clear(self):
        """Remove all events."""
        self.actionEvents.clear()
        self.nonActionEvents.clear()
    def getNonActionEvents(self):
        """Returns a list of all the events that do not need to wait until
        some player has a free action before they are processed."""
        return self.nonActionEvents
    def getFirstActionEvent(self, playerId):
        """Returns the first actionEvent (event which requires a player to
        have a free action) if there is one, or an empty list if there aren't
        any."""
        return self.actionEvents.get(playerId)
    def addEvent(self, event):
        if event.isActionEvent():
            assert isinstance(event, PlayerEvent)
            if event.playerId not in self.actionEvents:
                self.actionEvents[event.playerId] = event
        else:
            self.nonActionEvents.append(event)
    def addPygameEvents(self, pygameEvents, playerId):
        """Pass this the result of pygame.event.get() and it will add
        the corresponding events. The player-related ones will be tied
        to the specified playerId."""
        for pygameEvent in pygameEvents:
            if pygameEvent.type == pygame.QUIT:
                self.addEvent(QuitGameEvent())
            elif pygameEvent.type == pygame.KEYDOWN:
                keyCode = pygameKeyToKeyCode.get(pygameEvent.key)
                if keyCode is not None:
                    self.addEvent(KeyPressedEvent(playerId, keyCode))
            else:
                raise Exception(f"pygame event type {pygameEvent.type} not supported")

                
    
    
