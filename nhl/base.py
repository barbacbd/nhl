from json import dumps


class NHLBase:

    """
    Base class for the NHL classes. 
    """

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