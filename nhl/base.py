from json import dumps


class NHLBase:

    """
    Base class for the NHL classes. 
    """

    id = None
    name = None
    link = None

    def to_json(self):
        json_dir = {}
        for attr_name in dir(self):

            attr = getattr(self, attr_name)

            if not attr_name.startswith("_") and not callable(attr):
                if attr is not None:
                    if hasattr(attr, "to_json"):
                        json_dir[attr_name] = attr.to_json()
                    else:
                        json_dir[attr_name] = attr
        
        return json_dir

    
    def from_json(self, data):

        for k, v in data.items():
            if hasattr(self, k):
                if hasattr(getattr(self, k), "from_json"):
                    print(f"{self.__class__.__name__}, setting {k} to {v}")
                    attr = getattr(self, k)
                    attr.from_json(v)
                else:
                    print(f"{self.__class__.__name__}, setting {k} to {v}")
                    setattr(self, k, v)
    
    def __str__(self, *args, **kwargs):
        return dumps(self.to_json(), indent=4)