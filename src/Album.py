class Album:
    name = ""
    id = ""
    artist = ""

    def __init__(self, name, id, artist):
        self.name = name
        self.id = id
        self.artist = artist

    def __str__(self):
        return "%-20s" % "{}".format(self.name) + "by" + "%-10s" % "{}".format(self.artist) + " :- " + self.id

    def __unicode__(self):
            return u"%-20s" % "{}".format(self.name) + "by " + "%-10s" % "{}".format(self.artist) + " :- " + self.id
