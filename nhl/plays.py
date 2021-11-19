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
    
    """
    Goals is a simple object that only represents the 
    number of goals that the home and away team have at
    any moment.
    """

    away = None
    home = None


class PlayMetadata(NHLBase):
    
    """
    The play metadata is the section `about` in the document.
    The metadata contains all descriptive information about the
    play in reference to the entire game being played.
    """

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

    """
    The rink is roughly 200 ft by 85 ft for the nhl 
    standard rink (international rink sizes are slightly larger).
    The center is 0,0 and like the coordinate plane there exists
    a negative and positive x and y space.
    """

    x = None
    y = None


class EventPlayer(NHLBase):
    
    """
    An Event Player is an extension or a container around a player. It
    includes the player type in reference to the event. 
    Exmaple `playerTypes` may include `hitter`, `hittee`, etc.
    """

    player = None
    playerType = None
    
    def from_json(self, data):        
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

    players = None
    result = None
    about = None
    coordinates = None
    team = None
    
    
    def from_json(self, data):
        if "players" in data:
            self.players = []
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


    
    
    