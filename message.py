#
# A message is some text that can be displayed to the
# user. It will be displayed over the UI until the
# user dismisses it.
#

import pygame



class Message():
    """An object representing a message."""
    def __init__(self, text):
        """Create a Message, initializing it with the text to be displayed."""
        # FIXME: For now, we only allow one-line messages (but we'll fix that later).
        assert "\n" not in text
        self.text = text



class MessagePainter():
    """A singleton helper class that is used to render a message."""
    def __init__(self):
        self.fontName = "arial"
        self.fontSize = 24
        self.antialias = True
        self.fontColor = 0, 0, 0
        self.textBackgroundColor = 201, 246, 255
        self.textBorderSize = 5
        self.defaultFont = pygame.font.SysFont(self.fontName, self.fontSize)

    def paintMessage(self, surface, message):
        assert isinstance(message, Message)
        surfaceRect = surface.get_rect()
        line = message.text
        rendered = self.defaultFont.render(line, self.antialias, self.fontColor, self.textBackgroundColor)
        renderedRect = rendered.get_rect()
        renderedRect.center = surfaceRect.center
        backgroundRect = renderedRect.inflate(self.textBorderSize * 2, self.textBorderSize * 2)
        pygame.draw.rect(surface, self.textBackgroundColor, backgroundRect, 0)
        surface.blit(rendered, renderedRect)
