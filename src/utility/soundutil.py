from AppKit import NSSound  # exists
from Foundation import NSURL  # also exists so ignore


class SoundUtil:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def _canonicalizePath(self, path):
        """
        Support passing in a pathlib.Path-like object by converting to str.
        """
        import sys
        if sys.version_info[0] >= 3:
            return str(path)
        else:
            return path

    def _handlePathOSX(self, sound):
        sound = self._canonicalizePath(sound)

        if '://' not in sound:
            if not sound.startswith('/'):
                from os import getcwd
                sound = getcwd() + '/' + sound
            sound = 'file://' + sound

        try:
            # Don't double-encode it.
            sound.encode('ascii')
            return sound.replace(' ', '%20')
        except UnicodeEncodeError:
            try:
                from urllib.parse import quote  # Try the Python 3 import first...
            except ImportError:
                from urllib import quote  # Try using the Python 2 import before giving up entirely...

            parts = sound.split('://', 1)
            return parts[0] + '://' + quote(parts[1].encode('utf-8')).replace(' ', '%20')

    def build(self, path) -> NSSound:
        sound = self._handlePathOSX(path)
        url = NSURL.URLWithString_(sound)
        if not url:
            raise Exception('Cannot find a sound with filename: ' + sound)

        for i in range(5):
            nssound = NSSound.alloc().initWithContentsOfURL_byReference_(url, True)
            if nssound:
                break
        else:
            raise Exception('Could not load sound with filename, although URL was good... ' + sound)
        return nssound

    def play(self, song: NSSound, pos: float = 0.0):
        song.setCurrentTime_(pos)
        song.setVolume_(1.0)
        song.play()

    def pause(self, song: NSSound):
        song.pause()

    def resume(self, song: NSSound):
        song.resume()

    def stop(self, song: NSSound):
        song.stop()
