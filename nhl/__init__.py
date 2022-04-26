from json import dumps, loads
from typing import get_type_hints


class NHLBase:
    
    """
    Base class for the NHL classes. 
    """
    
    def __init__(self, data=None):
        self.hints = {}

    def register(self, class_type):
        """
        Register the class variables and their respective types.
        This function should be called after __init__ has finished for the
        base class AND all variables that should be registered are created
        in the child class.
        """
        self.hints = get_type_hints(class_type)
        
    @property
    def json(self):
        """Json or dictionary property

        Returns:
            dict: json dictionary filled with all non-none type values
        """
        data = {}
        for var in vars(self):
            item = getattr(self, var, None)
            if item is not None:
                data[var] = item

        return data
        
    @json.setter
    def json(self, data):
        """_summary_

        Args:
            data (dict): Json Dictionary object to be parsed into the instance variables
        """
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)

    def __str__(self):
        """Base string override that formats the data as json with clean indentation.

        Returns:
            str: Formatted json with 4 space indentation
        """
        return dumps(self.json, indent=4)



class Metadata(NHLBase):

    """
    The metadata is included for every game. This class includes 
    other variables that are NOT contained in any other json object, but
    could be considered metadata about the game including:
      - copyright
      - gamePk
      - link
    
    """

    def __init__(self):
        super().__init__()
        self.copyright:str = None
        self.gamePk:str = None
        self.link:str = None
        
        # contained in the metadata json object, could be extra fields in future
        self.wait:str = None
        self.timeStamp:str = None

        self.register()

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


class Game:

    """

    """

    def __init__(self):
        super().__init__()
        
        # NOTE: this may be int ...
        self.pk:str = None
        self.season: str = None
        self.type: str = None

        self.register()
        

class DateTime:

    """

    """

    def __init__(self):
        super().__init__()
        self.dateTime: str = None
        self.endDateTime: str = None
        self.register()

    @property
    def time(self):
        return None

    @property
    def endTime(self):
        return None
    

class Status:
    
    def __init__(self):    
        super().__init__()
        self.abstractGameState:str = None
        self.codedGameState:str = None
        self.detailedState:str = None
        self.statusCode:str = None
        self.startTimeTBD:bool = False
        self.register()
        

def create_from_file(filename):
    """_summary_

    Args:
        filename (_type_): _description_
    """
    if not filename.endswith(".json"):
        # log error
        return None

    with open(filename, "r") as f:
        json_data = loads(f.read())
    
    return create_from_json(json_data)
    
    
def create_from_json(contents):
    """_summary_

    Args:
        contents (_type_): _description_
    """
    if not isinstance(contents, dict):
        # log error
        return None
    
    meta = load_metadata(contents)
    
    # return info here
    return None


def load_metadata(contents):
    """_summary_

    Args:
        contents (_type_): _description_
    """
    meta = Metadata()
    meta.json = contents
    if "metaData" in contents:
        meta.json = contents["metaData"]
        
    return meta