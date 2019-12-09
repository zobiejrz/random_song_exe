class Song:
    name = ""
    artist = ""
    href = ""

    def __init__(self, name, artist, href):
        self.name = name
        self.artist = artist
        self.href = href

    def __str__(self):
        return "{} by {} {}".format(self.name, self.artist, self.href)
