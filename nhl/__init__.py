from json import dumps, loads
from typing import get_type_hints


class NHLBase:
    
    """
    Base class for the NHL classes. 
    """
    
    def __init__(self, data=None):
        self.hints = {}
        self.register()

    def register(self):
        """
        Register the class variables and their respective types.
        This function should be called after __init__ has finished for the
        base class AND all variables that should be registered are created
        in the child class.
        """
        if self.__class__.__name__ != NHLBase.__name__:
            print(self.__class__.__name__)
            print(get_type_hints(self.__class__))
            self.hints.update(get_type_hints(self.__class__))
        else:
            print("ERROR")
        
    @property
    def json(self):
        """Json or dictionary property

        Returns:
            dict: json dictionary filled with all non-none type values
        """
        data = {}
        for var in self.hints:
            print(var)
            item = getattr(self, var, None)
            if item is not None:
                data[var] = item

        print(data)

        return data
        
    @json.setter
    def json(self, data):
        """_summary_

        Args:
            data (dict): Json Dictionary object to be parsed into the instance variables
        """
        print(data)
        for k, v in data.items():
            print(k)
            if k in self.hints:
                #if hints is a basic type cast it here, otherwise figure it out
                print(self.hints[k])
                print(v)
                # setattr(self, k, self.hints[k](v))

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
    copyright:str = None
    gamePk:str = None
    link:str = None
    
    # contained in the metadata json object, could be extra fields in future
    wait:str = None
    timeStamp:str = None

    def __init__(self):
        super().__init__()

    @property
    def json(self):
        meta= {"wait": self.wait, "timeStamp": self.timeStamp}

        data = {}
        for var in set(vars(self)).difference(set(list(meta.keys()) + ['hints'])):
            print(var)
            item = getattr(self, var, None)

            if item is not None:
                data[var] = item

        for k, v in meta.copy().items():
            if v is None:
                meta.pop(k)

        print(data)
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

    pk:str = None
    season: str = None
    type: str = None

    def __init__(self):
        super().__init__()
                

class DateTime:

    """

    """

    dateTime: str = None
    endDateTime: str = None

    def __init__(self):
        super().__init__()

    @property
    def time(self):
        return None

    @property
    def endTime(self):
        return None
    

class Status:

    """
    
    """
    
    abstractGameState:str = None
    codedGameState:str = None
    detailedState:str = None
    statusCode:str = None
    startTimeTBD:bool = False
    
    def __init__(self):    
        super().__init__()
        

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


with open("../database/nhl_data/2021/2021_1.json", "r") as f:
    jd = loads(f.read())


x = Metadata()
# print(jd["metaData"])
x.json = jd
x.json = jd["metaData"]

print(str(x))