from json import dumps


class Position:

    code = None
    name = None
    type = None
    abbreviation = None

    @property
    def json(self):
        attempt = {
            "code": self.code,
            "name": self.name,
            "type": self.type,
            "abbreviation": self.abbreviation
        }

        return {k: v for k, v in attempt.items() if v is not None}


    @json.setter
    def json(self, data):
        for k, v in data.items():
            if k in self.__slots__:
                setattr(self, k, v)
    
    def __str__(self, *args, **kwargs):
        return dumps(self.json, indent=4)
        
        
class Player:

    id = None
    firstName = None
    lastName = None
    primaryNumber = None
    birthDate = None
    active = False
    captain = False
    alternativeCaptain = False
    rookie = False
    shootsCatches = None
    primaryPosition = Position()

    @property
    def json(self):
        
        json_dir = {}
        for attr_name in dir(self):

            attr = getattr(self, attr_name)

            if not attr_name.startswith("_") and not callable(attr):
                if attr is not None:
                    if hasattr(attr, "json"):
                        json_dir[attr_name] = attr.json
                    else:
                        json_dir[attr_name] = attr
        
        return json_dir
    
    @json.setter
    def json(self, data):

        for k, v in data.items():
            if hasattr(self, k):
                if hasattr(getattr(self, k), "json"):
                    getattr(self, k).json = v
                else:
                    setattr(self, k, v)
    
    def __str__(self, *args, **kwargs):
        return dumps(self.json, indent=4)
    