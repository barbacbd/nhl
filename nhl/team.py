from .base import NHLBase


class Venue(NHLBase):

    """
    Class to describe the arena in which a team plays
    """

    class TimeZone(NHLBase):
        id = None
        offset = None
        cz = None

    id = None
    name = None
    link = None
    city = None
    timeZone = TimeZone()


class Team(NHLBase):

    """
    Class to describe the nhl team
    """

    id = None
    name = None
    link = None
    venue = Venue()

    abbreviation = None
    triCode = None
    teamName = None
    locationName = None
    firstYearOfPlay = 1917  # first year of stanley cup
    #division = Division()
    #conference = Conference()
    #franchise = Franchise()
    shortName = None
    officialSiteUrl = None
    franchiseId = None
    active = False
