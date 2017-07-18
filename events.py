import pygame

    

class Event:
    """Parent class for all events."""
    def isActionEvent(self):
        """Returns True if this event can only be processed when the player
        has an action and False otherwise."""
        return False

class QuitGameEvent(Event):
    """An event for when the game is going to exit (on the server)."""
    pass

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
        return True

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
        self.actionEvents = []
        self.nonActionEvents = []
    def clear(self):
        """Remove all events."""
        self.actionEvents.clear()
        self.nonActionEvents.clear()
    def addEvent(self, event):
        if event.isActionEvent():
            self.actionEvents.append(event)
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
                self.addEvent(KeyPressedEvent(playerId, pygameEvent.key))
            else:
                raise Exception(f"pygame event type {pygameEvent.type} not supported")

                
    
    
