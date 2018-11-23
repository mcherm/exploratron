
import pygame
import os

TILE_SIZE = 64


class LibraryWithIds:
    """For both images and sounds, we want to refer to the media using names
    (strings that match up with the filenames), but when we pass references to
    the media across the network we want a briefer way to refer to them. This
    library provides that, converting from names to IDs and allowing a lookup
    by ID."""
    def __init__(self, rootDir, extension, subdir):
        """This will walk all files in the given subdir of the given rootDir, and treat
        any file ending in the given extension as a media source."""
        extensionLen = len(extension)
        self.mediaById = {}
        self._idByName = {}
        for root, dirs, files in os.walk(f'{rootDir}/{subdir}'):
            files.sort() # important to sort them so the order is consistent
            counter = 0
            for file in files:
                if file.endswith(extension):
                    name = file[:-extensionLen] # trim off the extension
                    tileId = counter
                    self._idByName[name] = tileId
                    self.mediaById[tileId] = self.loadMedia(f'{rootDir}/{subdir}/{name}{extension}')
                    counter += 1
    def loadMedia(self, filename):
        pass # Subclasses need to implement this
    def lookupById(self, mediaId):
        return self.mediaById[mediaId]
    def idByName(self, mediaName):
        return self._idByName[mediaName]


class ImageLibrary(LibraryWithIds):
    def __init__(self, subdir):
        super().__init__(rootDir='./img', extension='.png', subdir=subdir)
    def loadMedia(self, filename):
        return pygame.image.load(filename)


class SoundLibrary(LibraryWithIds):
    def __init__(self, subdir):
        super().__init__(rootDir='./sound', extension='.wav', subdir=subdir)
    def loadMedia(self, filename):
        try:
            return pygame.mixer.Sound(filename)
        except pygame.error as err:
            raise Exception(f"Unable to load sound '{filename}'. Are you sure that init() was called?") from err



class Region:
    """Someday, this might grow into the ability to have different
    regions with their own sets of rooms and their own image libraries."""
    def __init__(self):
        pygame.init() # FIXME: if there are multiple regions, need to init() only before the first one
        self.imageLibrary = ImageLibrary('drawntiles64')
        self.soundLibrary = SoundLibrary('foundassets/freesound.org')
