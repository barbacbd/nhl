from .base import NHLBase


class Venue(NHLBase):

    """
    Class to describe the arena in which a team plays
    """

    class TimeZone(NHLBase):
        offset = None
        cz = None

    city = None
    timeZone = None

    def from_json(self, data):

        if "timeZone" in data:
            self.timeZone = Venue.TimeZone(data["timeZone"])

        super().from_json(data)


class Franchise(NHLBase):

    franchiseId = None
    teamName = None


class Team(NHLBase):

    """
    Class to describe an NHL team. 
    """

    venue = None
    abbreviation = None
    triCode = None
    teamName = None
    locationName = None
    firstYearOfPlay = None
    division = None
    conference = None
    franchise = None
    shortName = None
    officialSiteUrl = None
    franchiseId = None
    active = None

    def from_json(self, data):
        
        if "venue" in data:
            self.venue = Venue(data["venue"])
        
        if "division" in data:
            self.division = NHLBase(data["division"])
        
        if "conference" in data:
            self.conference = NHLBase(data["conference"])
        
        if "franchise" in data:
            self.franchise = Franchise(data["franchise"])
        
        super().from_json(data)