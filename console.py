#
# A console is an area on the screen where a series of text messages can be
# shown. It is designed to work only with fixed-width fonts (to make it much
# easier to build). It shows only the most recent messages, with others
# scrolling off the top.
#

import pygame

FONT_FILE = "font/Code New Roman.otf"
FONT_SIZE = 18
ANTIALIAS = True
TEXT_COLOR = (250, 250, 250)
BACKGROUND_COLOR = (20, 20, 20)
NUMBER_OF_MESSAGES_TO_KEEP = 150


_theFont = None
_theFontCharWidth = None
_theFontCharHeight = None


def initializeFont():
    global _theFont
    global _theFontCharWidth
    global _theFontCharHeight
    if _theFont is None:
        _theFont = pygame.font.Font(FONT_FILE, FONT_SIZE)
    surface = _theFont.render("x", ANTIALIAS, TEXT_COLOR, BACKGROUND_COLOR)
    _theFontCharWidth = surface.get_width()
    _theFontCharHeight = surface.get_height()


def getFont():
    """This retrieves the (one and only, fixed-width) font used in the Console. It
    uses _theFont as a storage for lazy-loading this."""
    initializeFont()
    return _theFont


def charWidthInPixels():
    """Get the number of pixels wide that the fixed-width font is."""
    initializeFont()
    return _theFontCharWidth


def charHeightInPixels():
    """Get the number of pixels tall that the font is."""
    initializeFont()
    return _theFontCharHeight


class Console():
    """An area on the screen where a series of messages can be displayed."""
    def __init__(self, sizeInPixels):
        """Constructor. Caller must specify an initial size in pixels as a
        (width, height) tuple."""
        getFont() # make sure the font has been loaded
        self.resize(sizeInPixels)
        self.messages = []
        self.lines = None
        self.background = None

    def resize(self, sizeInPixels):
        """This is passed a (width, height) tuple giving a new size that the console should
        change to."""
        self.sizeInPixels = sizeInPixels
        self.widthInChars = sizeInPixels[0] // charWidthInPixels()
        self.heightInChars = sizeInPixels[1] // charHeightInPixels()
        self._invalidate()


    def _invalidate(self):
        """Call this when the layout has changed for some reason."""
        self.background = None
        self.lines = None

    def addMessage(self, message):
        self.messages.append(message)
        if len(self.messages) > NUMBER_OF_MESSAGES_TO_KEEP * 1.1:
            del self.messages[:-NUMBER_OF_MESSAGES_TO_KEEP]
        self._invalidate()

    def _lineWrap(self):
        """This should be called with self.lines is None and we need it set. It goes
        through the most recent messages and line-wraps them to fit."""
        lines = [] # we'll collect them in order
        messagesReversed = reversed(self.messages)
        while len(lines) < self.heightInChars:
            try:
                message = messagesReversed.__next__()
            except StopIteration:
                break # out of the while loop because we've got all the messages
            linesForThisMessage = []
            messageLength = len(message)
            startOfThisLine = 0
            while messageLength - startOfThisLine > 0:
                if message[startOfThisLine] == " ":
                    startOfThisLine += 1
                else:
                    if messageLength - startOfThisLine <= self.widthInChars:
                        # the rest fits on one line
                        endOfThisLine = messageLength
                    else:
                        lastSpacePosition = message.rfind(" ", startOfThisLine, startOfThisLine + self.widthInChars)
                        if lastSpacePosition == -1:
                            # was no space; break at width of the screen
                            endOfThisLine = startOfThisLine + self.widthInChars
                        else:
                            # break at the last space that will fit
                            endOfThisLine = lastSpacePosition
                    line = message[startOfThisLine:endOfThisLine].rstrip()
                    if line:
                        linesForThisMessage.append(line)
                    startOfThisLine = endOfThisLine
            lines.extend(reversed(linesForThisMessage))

        lines.reverse() # put back in normal order
        self.lines = lines


    def _createBackground(self):
        background = pygame.Surface(self.sizeInPixels)
        background = background.convert()
        background.fill(BACKGROUND_COLOR)

        if self.lines is None:
            self._lineWrap()
        linesRendered = 0
        for line in self.lines[-self.heightInChars:]:
            lineAsSurface = getFont().render(line, ANTIALIAS, TEXT_COLOR)
            position = lineAsSurface.get_rect()
            position.top = linesRendered * charHeightInPixels()
            background.blit(lineAsSurface, position)
            linesRendered += 1

        self.background = background

    def show(self, surface, position):
        """This is called when the Console should be painted to the screen. It draws
        the current text to the surface within the rect position. position is expected to
        match the known size of the console."""
        assert (position.width, position.height) == self.sizeInPixels
        if self.background is None:
            self._createBackground()
        surface.blit(self.background, (position.left, position.top))


def runFramework():
    INITIAL_SIZE = (300, 130)

    from pygame.locals import QUIT
    pygame.init()
    screen = pygame.display.set_mode(INITIAL_SIZE)
    pygame.display.set_caption("Example Program")

    console = Console(INITIAL_SIZE)
    console.addMessage("Hello, world.")
    console.addMessage("This is a longer linnnnnnnnnnnnnnnnnnnnnnnnnnnnnne that we want to see wrapped.")
    console.addMessage("Let's make it longer.")
    console.addMessage("One more.")
    console.addMessage("And a last line.")

    resized = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                if resized:
                    return
                else:
                    pygame.display.set_mode((400,130))
                    console.resize((400,130))
                    resized = True
        console.show(screen, screen.get_rect())
        pygame.display.flip()



def try_custom_font():
    from pygame.locals import QUIT
    pygame.init()
    screen = pygame.display.set_mode((200,100))
    pygame.display.set_caption("Example Program")


    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    font = pygame.font.Font(FONT_FILE, FONT_SIZE)
    text = font.render("Hello There", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(text, textpos)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        screen.blit(background, (0,0))
        pygame.display.flip()


if __name__ == "__main__":
    runFramework()
