from json import dumps, loads
from typing import get_type_hints
from logging import getLogger
from os.path import exists


log = getLogger()


class NHLData:
    
    def __init__(self, data):
        self.__children = set()
        self.__keys = {}
        
        self.load(data)
    
    def load(self, data):
        """Load the data from a dictionary

        Args:
            data (dict): Json formatted dictionary

        """
        if not isinstance(data, dict):
            log.error("data was not a dictionary")
        else:
            for k, v in data.items():
                self.__children.add(k.lower())
                self.__keys[k.lower()] = k
                # Add the children to this node in the structure
                if isinstance(v, dict):
                    setattr(self, k, NHLData(v))
                else:
                    setattr(self, k, v)
    
    def query(self, qdata):
        """Search the NHL Data tree by looking at the children to find the value associated with
        the output. The output with be a simple type OR NHLData object

        Example:
            data = query(['this', 'is', 'a', 'test'])
            data would contain whatever information was stored at 
            ```
            {
                "this": {
                    "is": {
                        "a": {
                            "test" : {
                                
                            }
                        }
                    }
                }
            }
            ```

        Args:
            qdata (str, list(str)): A string seperated by `.` or a list of ordered words.

        Returns:
            simple (json serializable type) or NHLData: When found return the found data
        """
        if isinstance(qdata, str):
            qdataCopy = qdata.split(".")
        elif isinstance(qdata, list):
            qdataCopy = qdata.copy()
        else:
            log.error("Suggested format is a list of string or a string delimited by periods.")
            return None

        # child is the first element in the list
        child = qdataCopy.pop(0)

        if child.lower() in self.__children:
            realName = self.__keys[child.lower()]
            
            if len(qdataCopy) > 0:
                return getattr(self, realName).query(qdataCopy)
            else:
                return getattr(self, realName)
        else:
            log.error("Failed to find {} in children.".format(child))
            return None
    
    @property
    def children(self):
        """Interface to get all children of this instance

        Returns:
            list: List of all children
        """
        return list(self.__keys.values())
    
    @property
    def json(self):
        """Json property that provides the data stored in this instance as
        a json formatted dictionary
        """
        d = {}
        for var in vars(self):
            if not var.startswith("_") and not callable(getattr(self, var)):
                
                val = getattr(self, var)
                if val is not None:
                    if isinstance(val, NHLData):
                        d[var] = val.json
                    else:
                        d[var] = val

        return d
    
    def tree(self, indent=0):
        """Provide the Tree report that contains the children
        formatted for the user to see. This is not the same as the
        json data, as no values are provided.
        
        Example Output:
        ```
        example
          |
          -- child_1
          -- child_2
            |
            -- grandchild_1
        example_2
          |
          -- child_1
        ```
        
        Returns:
            str: A simple tree structure that indicates parents and children
        
        """
        treeStr = ""
        treeDent = "  " * (indent-1)
        if indent > 1:
            treeDent += "--"
        
        childInd = "  " * (indent) + "|"
        for alias in self.__children:
            child = self.__keys[alias]
            treeStr += "{}{}\n".format(treeDent, child)
            
            if isinstance(getattr(self, child), NHLData):
                treeStr += childInd + "\n"
                treeStr += getattr(self, child).tree(indent+1)
            
        return treeStr            
    
    def __str__(self):
        """String override

        Returns:
            str: Json String representation
        """
        return dumps(self.json, indent=4)


def ParseFromContents(data):
    """Create a base NHLData object that will hold everything in the 
    dictionary

    Args:
        data (dict): Parse the contents of the data.
    
    Returns:
        NHLData object. In the event of bad data, the object will be empty but the
        shell of an NHLData Object will remain
    """
    return NHLData(data)


def ParseFromFile(filename):
    """Parse the contents of the File

    Args:
        filename (str): full path to the file containing json data
    
    Returns:
        NHLData object when successful, otherwise None.
        
    Note: A successful return is NOT an indicator of a full success. See `ParseFromContents` for
    more information.
    """
    if filename.endswith(".json") and exists(filename):
        with open(filename, "r") as f:
            jd = loads(f.read())
        
        return ParseFromContents(jd)

