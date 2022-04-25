from json import dumps


class Metadata:

    """
    The metadata is included for every game. This class includes 
    other variables that are NOT contained in any other json object, but
    could be considered metadata about the game including:
      - copyright
      - gamePk
      - link
    
    """

    def __init__(self):
        self.copyright = None
        self.gamePk = None
        self.link = None
        
        # contained in the metadata json object, could be extra fields in future
        self.wait = None
        self.timeStamp = None

    @property
    def json(self):
        meta= {"wait": self.wait, "timeStamp": self.timeStamp}

        data = {}
        for var in set(vars(self)).difference(set(list(meta.keys()))):
            item = getattr(self, var, None)

            if item is not None:
                data[var] = item

        for k, v in meta.copy().items():
            if v is None:
                meta.pop(k)

        if meta:
            data["metaData"] = meta

        return data
        
    @json.setter
    def json(self, data):
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)

    def __str__(self):
        return dumps(self.json, indent=4)


class GameData:

    """

    """

    def __init__(self):

        self.game = None
        self.datetime = None
        self.status = None
        self.teams = None
        self.players = None
        self.venue = None
