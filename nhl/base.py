from json import dumps


class NHLBase:

    """
    Base class for the NHL classes. 
    """

    id = None
    name = None
    link = None

    def __init__(self, data=None):
        if isinstance(data, dict):
            self.from_json(data)

    def to_json(self):
        json_dir = {}
        for attr_name in dir(self):

            attr = getattr(self, attr_name)

            if not attr_name.startswith("_") and not callable(attr):
                if attr is not None:

                    if isinstance(attr, list):
                        print(f"{attr_name} is a list")
                        print(f" here it is {attr}")
                        json_dir[attr_name] = []
                        
                        for a in attr:
                            if hasattr(a, "to_json"):
                                json_dir.append(a.to_json())
                            else:
                                json_dir.append(a)
                    else:
                        if hasattr(attr, "to_json"):
                            json_dir[attr_name] = attr.to_json()
                        else:
                            json_dir[attr_name] = attr
        
        return json_dir

    
    def from_json(self, data):

        for k, v in data.items():
            if hasattr(self, k):
                # Indicates that this is another object, but only set it if its not set currently
                if hasattr(getattr(self, k), "from_json") and getattr(self, k, None) is None:
                    attr = getattr(self, k)
                    attr.from_json(v)
                else:
                    setattr(self, k, v)
    
    def __str__(self, *args, **kwargs):
        return dumps(self.to_json(), indent=4)