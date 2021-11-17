from .base import NHLBase
from .team import Team
        

class Stats(NHLBase):

    """
    Box score statistics for a player. 
    """

    # common player game stats information
    timeOnIce = None
    assists = None
    goals = None
    shots = None
    
    # goalie game stats information
    pim = None
    saves = None
    powerPlaySaves = None
    shortHandedSaves = None
    evenSaves = None
    shortHandedShotsAgainst = None
    evenShotsAgainst = None
    powerPlayShotsAgainst = None
    decision = None
    savePercentage = None
    powerPlaySavePercentage = None
    evenStrengthSavePercentage = None

    # skater game Stats information
    hits = None
    powerPlayGoals = None
    powerPlayAssists = None
    penaltyMinutes = None
    faceOffWins = None
    faceoffTaken = None
    takeaways = None
    giveaways = None
    shortHandedGoals = None
    shortHandedAssists = None
    blocked = None
    plusMinus = None
    evenTimeOnIce = None
    powerPlayTimeOnIce = None
    shortHandedTimeOnIce = None
    


class Player(NHLBase):

    class Position(NHLBase):
        
        """
        Class to describe a players position on ice
        """
        
        code = None
        name = None
        type = None
        abbreviation = None

    """
    A class to represent an NHL player. This will include
    Defensemen, Wingers, Centers, goalies, etc.
    """

    fullName = None
    firstName = None
    lastName = None
    primaryNumber = None
    birthDate = None
    currentAge = 0
    birthCity = None
    birthCountry = None
    nationality = None
    height = None
    weight = None
    active = False
    alternativeCaptain = False
    captain = False
    rookie = False
    shootsCatches = None
    rosterStatus = None
    currentTeam = Team()
    primaryPosition = Position()
    stats = None
