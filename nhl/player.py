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
    currentAge = None
    birthCity = None
    birthCountry = None
    nationality = None
    height = None
    weight = None
    active = None
    alternativeCaptain = None
    captain = None
    rookie = None
    shootsCatches = None
    rosterStatus = None
    currentTeam = None
    primaryPosition = None
    stats = None


    def from_json(self, data):

        if "currentTeam" in data:
            self.currentTeam = Team(data["currentTeam"])
        
        if "primaryPosition" in data:
            self.primaryPosition = Player.Position(data["primaryPosition"])

        # allow the parent to handle the rest
        super().from_json(data)