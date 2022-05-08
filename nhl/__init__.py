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

        :param data: Json formatted dictionary
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

        :param qdata: A string seperated by `.` or a list of ordered words.
        :return: simple (json serializable type) or NHLData: When found return the found data
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

        :return: List of all children
        """
        return list(self.__keys.values())
    
    @property
    def json(self):
        """Json property that provides the data stored in this instance as
        a json formatted dictionary
        
        :return: JSON Serialized Dictionary
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
        
        :return: A simple tree structure that indicates parents and children
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

        :return: Json String representation
        """
        return dumps(self.json, indent=4)


def ParseFromContents(data):
    """Create a base NHLData object that will hold everything in the 
    dictionary

    :param data: Parse the contents of the data.
    :return: NHLData object or None on faillure.
    """
    return NHLData(data)


def ParseFromFile(filename):
    """Parse the contents of the File

    :param filename: full path to the file containing json data
    :return: NHLData object when successful, otherwise None.
    """
    if filename.endswith(".json") and exists(filename):
        with open(filename, "r") as f:
            jd = loads(f.read())
        
        return ParseFromContents(jd)
