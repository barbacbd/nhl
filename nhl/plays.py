from .base import NHLBase
from .player import Player
from .team import Team
from collections import defaultdict


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
    
    player = None
    playerType = None
    
    def from_json(self, data):
        
        if "player" in data:
            self.player = Player()
            self.player.from_json(data["player"])
        
        if "playerType" in data:
            self.playerTyper = data["playerType"]


class Play(NHLBase):

    """
    Every Play is documented for every NHL Game. This class
    represents the entire breakdown of the play including all players
    involved, the result, metadata, where the event happened, and 
    the team involved.
    """

    players = []  # list of EventPlayers
    result = None
    about = None
    coordinates = None
    team = None
    
    
    def from_json(self, data):
        # empty the current list of players
        self.players.clear()
        
        if "players" in data:
            for player_data in data["players"]:
                p = EventPlayer()
                p.from_json(player_data)
                self.players.append(p)
        
        if "result" in data:
            self.result = Result()
            self.result.from_json(data["result"])
        
        if "about" in data:
            self.about = PlayMetadata()
            self.about.from_json(data["about"])
        
        if "coordinates" in data:
            self.coordinates = Coordinates()
            self.coordinates.from_json(data["coordinates"])
        
        if "team" in data:
            self.team = Team()
            self.team.from_json(data["team"])


class PlayTypeTracker:

    scoringPlays = []
    penaltyPlays = []
    playsByPeriod = defaultdict(list)


    
    
    