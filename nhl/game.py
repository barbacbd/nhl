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


class TeamPeriodData(NHLBase):
    goals = 0
    shotsOnGoal = 0
    attempts = 0
    rinkSide = None


class Period(NHLBase):
    
    periodType = None
    startTime = None
    endTime = None
    num = None
    ordinalNum = None
    home = TeamPeriodData()
    away = TeamPeriodData()


class ShootoutInfo(NHLBase):
    
    home = TeamPeriodData()
    away = TeamPeriodData()


class Linescore(NHLBase):
    
    currentPeriod = 0
    currentPeriodOrdinal = None
    currentPeriodTimeRemaining = None
    periods = []