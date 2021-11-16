from .base import NHLBase
from .team import Team


class Position(NHLBase):

    code = None
    name = None
    type = None
    abbreviation = None
        
        
class Player(NHLBase):

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
