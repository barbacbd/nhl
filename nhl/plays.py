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
    
    away = None
    home = None


class PlayMetadata(NHLBase):
    
    eventIdx = None
    eventId = None	
    period = None
    periodType = None
    ordinalNum = None
    periodTime = None
    periodTimeRemaining = None
    dateTime = None
    goals = None

    def from_json(self, data):

        if "goals" in data:
            self.goals = Goals(data["goals"])
        
        super().from_json(data)


class Coordinates(NHLBase):

    x = None
    y = None


class EventPlayer(NHLBase):
    
    player = None
    playerType = None
    
    def from_json(self, data):
        
        print(f"Player Data {data}")

        if "player" in data:
            self.player = Player(data["player"])
        
        super().from_json(data)


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
                self.players.append(EventPlayer(player_data))
        
        if "result" in data:
            self.result = Result(data["result"])
        
        if "about" in data:
            self.about = PlayMetadata(data["about"])
        
        if "coordinates" in data:
            self.coordinates = Coordinates(data["coordinates"])
        
        if "team" in data:
            self.team = Team(data["team"])


class PlayTypeTracker:

    scoringPlays = []
    penaltyPlays = []
    playsByPeriod = defaultdict(list)


    
    
    