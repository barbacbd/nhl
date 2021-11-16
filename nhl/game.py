from .base import NHLBase


class Game(NHLBase):

    pk = None
    season = None
    type = None


class DateTime(NHLBase):
    
    dateTime = None
    endDateTime = None
    

class Status(NHLBase):

    abstractGameState = None
    codedGameState = 0
    detailedState = None
    statusCode = 0
    startTimeTBD = False

