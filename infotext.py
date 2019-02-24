#
# A message is some text that can be displayed to the
# user. It will be displayed over the UI until the
# user dismisses it.
#

import pygame



class InfoText():
    """An object representing an informational text to show to the user."""
    def __init__(self, text):
        """Create an InfoText, initializing it with the text to be displayed."""
        self.lines = text.splitlines()

    def getLines(self):
        """Returns a list of strings, each containing one line from the info text."""
        # FIXME: In the future, we might want to support text wrapping, in which case
        # FIXME:   this will need some information to perform that wrapping.
        return self.lines

    def getText(self):
        """Returns a single string containing the content, without wrapping.
        Forced returns will be represented as a "\n" within the string."""
        return "\n".join(self.lines)


MESSAGE_FONT = "arial"
MESSAGE_FONT_SIZE = 24
MESSAGE_FONT_ANTIALIAS = True
MESSAGE_TEXT_COLOR = 0, 0, 0
MESSAGE_BACKGROUND_COLOR = 201, 246, 255
MESSAGE_TEXT_BORDER = 5


class InfoTextPainter:
    """A singleton helper class that is used to render a message."""
    def __init__(self):
        self.defaultFont = pygame.font.SysFont(MESSAGE_FONT, MESSAGE_FONT_SIZE)

    def paintInfoText(self, surface, infoText):
        assert isinstance(infoText, InfoText)

        # -- render each line in the proper font --
        lines = infoText.getLines()
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
