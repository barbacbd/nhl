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
    codedGameState = None
    detailedState = None
    statusCode = None
    startTimeTBD = False


class TeamPeriodData(NHLBase):
    goals = None
    shotsOnGoal = None
    attempts = None
    rinkSide = None


class Period(NHLBase):
    
    periodType = None
    startTime = None
    endTime = None
    num = None
    ordinalNum = None
    home = None
    away = None

    def from_json(self, data):

        if "home" in data:
            self.home = TeamPeriodData(data["home"])
        
        if "away" in data:
            self.away = TeamPeriodData(data["away"])

        super().from_json(data)


class ShootoutInfo(NHLBase):
    
    home = None
    away = None

    def from_json(self, data):

        if "home" in data:
            self.home = TeamPeriodData(data["home"])
        
        if "away" in data:
            self.away = TeamPeriodData(data["away"])


class Linescore(NHLBase):
    
    currentPeriod = None
    currentPeriodOrdinal = None
    currentPeriodTimeRemaining = None
    periods = []
    

class FinalGamePlays(NHLBase):
    
    scoringPlays = []
    penaltyPlays = []
    playsByPeriod = {}
    


