import pygame
from console import FONT_FILE, FONT_SIZE, ANTIALIAS, TEXT_COLOR, BACKGROUND_COLOR, getFont, charWidthInPixels, \
        charHeightInPixels, Console


def test_canLoadFont():
    pygame.init()
    font = pygame.font.Font(FONT_FILE, FONT_SIZE)


def test_calculateCharWidth():
    pygame.init()
    TEST_STRINGS = ["X", "XXXXXXXXXX", "xxxxxxxx", ".....", "abcdefg", "ABCDEFG"]
    for test_str in TEST_STRINGS:
        renderedLine = getFont().render(test_str, ANTIALIAS, TEXT_COLOR, BACKGROUND_COLOR)
        assert renderedLine.get_width() == len(test_str) * charWidthInPixels()

def test_calculateCharHeight():
    pygame.init()
    TEST_STRINGS = ["X", "XXXXXXXXXX", "xxxxxxxx", ".....", "abcdefg", "ABCDEFG"]
    for test_str in TEST_STRINGS:
        renderedLine = getFont().render(test_str, ANTIALIAS, TEXT_COLOR, BACKGROUND_COLOR)
        assert renderedLine.get_height() == charHeightInPixels()


def wordWrapExperiment(messages, expectedLines):
    pygame.init()
    LINE_LEN = 5
    ROWS = 20
    console = Console((LINE_LEN * charWidthInPixels(), ROWS * charHeightInPixels()))
    assert console.widthInChars == LINE_LEN
    assert console.heightInChars == ROWS
    for message in messages:
        console.addMessage(message)
    console._lineWrap()
    assert console.lines == expectedLines

def test_wordWrap_longword():
    wordWrapExperiment(["abcdefg"], ["abcde", "fg"])

def test_wordWrap_wordJustFitsLine():
    wordWrapExperiment(["abcde"], ["abcde"])

def test_wordWrap_barelyTooShort():
    wordWrapExperiment(["abcd"], ["abcd"])

def test_wordWrap_veryShort():
    wordWrapExperiment(["a"], ["a"])

def test_wordWrap_wrap1():
    wordWrapExperiment(["abcd fgh"], ["abcd", "fgh"])

def test_wordWrap_wrap2():
    wordWrapExperiment(["abcde ghi"], ["abcde", "ghi"])

def test_wordWrap_wrap3():
    wordWrapExperiment(["abcd  ghi"], ["abcd", "ghi"])

def test_wordWrap_wrap4():
    wordWrapExperiment(["abc   ghi"], ["abc", "ghi"])

def test_wordWrap_wrap5():
    wordWrapExperiment(["ab    ghi"], ["ab", "ghi"])

def test_wordWrap_wrap6():
    wordWrapExperiment(["ab   fgh"], ["ab", "fgh"])

def test_wordWrap_wrap7():
    wordWrapExperiment(["ab  efg"], ["ab", "efg"])

def test_wordWrap_wrap8():
    wordWrapExperiment(["ab def"], ["ab", "def"])

def test_wordWrap_wrap9():
    wordWrapExperiment(["ab de"], ["ab de"])

def test_wordWrap_leadingSpaces():
    wordWrapExperiment([" ab"], ["ab"])

def test_wordWrap_justSpaces():
    wordWrapExperiment(["  "], [])

def test_wordWrap_longSpace():
    wordWrapExperiment(["abc       klm"], ["abc", "klm"])

def test_wordWrap_longTextLine2():
    wordWrapExperiment(["abc efghijkl no"], ["abc", "efghi", "jkl", "no"])

def test_wordWrap_emptyMessage():
    wordWrapExperiment([""], [])
