from .base import NHLBase
from .player import Player
from .team import Team


class Result(NHLBase):
    event = None
    eventCode = None
    eventTypeId = None
    description = None


class Goals(NHLBase):
    
    away = 0
    home = 0


class PlayMetadata(NHLBase):
    
    eventIdx = 0
    eventId = 0
    period = 0
    periodType = None
    ordinalNum = None
    periodTime = None
    periodTimeRemaining = None
    dateTime = None
    goals = Goals()


class Coordinates(NHLBase):

    x = 0.0
    y = 0.0    


class EventPlayer(NHLBase):
    
    player = Player()
    playerType = None


class Play(NHLBase):

    players = []  # list of EventPlayers
    result = Result()
    about = PlayMetadata()
    coordinates = None
    team = None
    
    
    def from_json(self, data):
        pass


    
    
    