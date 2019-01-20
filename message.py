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
        self.lines = text.splitlines()

    def getLines(self):
        """Returns a list of strings, each containing one line from the message."""
        # FIXME: In the future, we might want to support text wrapping, in which case
        # FIXME:   this will need some information to perform that wrapping.
        return self.lines


MESSAGE_FONT = "arial"
MESSAGE_FONT_SIZE = 24
MESSAGE_FONT_ANTIALIAS = True
MESSAGE_TEXT_COLOR = 0, 0, 0
MESSAGE_BACKGROUND_COLOR = 201, 246, 255
MESSAGE_TEXT_BORDER = 5


class MessagePainter:
    """A singleton helper class that is used to render a message."""
    def __init__(self):
        self.defaultFont = pygame.font.SysFont(MESSAGE_FONT, MESSAGE_FONT_SIZE)

    def paintMessage(self, surface, message):
        assert isinstance(message, Message)

        # -- render each line in the proper font --
        lines = message.getLines()
        renderedLines = [
            self.defaultFont.render(line, MESSAGE_FONT_ANTIALIAS, MESSAGE_TEXT_COLOR, MESSAGE_BACKGROUND_COLOR)
            for line in lines]

        # -- determine the position of the text --
        maxWidth = max(x.get_width() for x in renderedLines)
        lineHeight = renderedLines[0].get_height() # Assuming all are the same height
        textRect = pygame.Rect(0, 0, maxWidth, lineHeight * len(lines))
        textRect.center = surface.get_rect().center

        # -- draw the background --
        backgroundRect = textRect.inflate(MESSAGE_TEXT_BORDER * 2, MESSAGE_TEXT_BORDER * 2)
        pygame.draw.rect(surface, MESSAGE_BACKGROUND_COLOR, backgroundRect, 0)

        # -- copy each line into position --
        linePositionY = textRect.top
        for renderedLine in renderedLines:
            surface.blit(renderedLine, (textRect.left, linePositionY))
            linePositionY += lineHeight
