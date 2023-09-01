from enum import Enum
from datetime import datetime


# The first season of the NHL was 1917 but some teams played in leagues prior to the
# formation of the NHL.
NHL_FIRST_SEASON = 1917

# Initializing the number of games during the regular season to number of teams * 41
# due to 41 home games. This value can and should be overwritten as more teams enter
# the league or the season length changes.
MAX_GAME_NUMBER = 1312

# 
# Base Endpoints
#
API_TEAM_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/teams"
API_DIVISION_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/divisions"
API_CONFERENCE_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/conferences"

API_STANDINGS_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/standings"
API_STANDINGTYPES_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/standingsTypes"
API_STATTYPES_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/statTypes"
_API_TEAMSTATS_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/teams/{}/stats"
API_DRAFT_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/draft"
API_PROSPECTS_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/prospects"
API_AWARDS_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/awards"


_TEAM_MODIFIERS = {
    "roster": None,
    "names": None,
    "next": None,
    "previous": None,
    "stats": None,
    "season": str,
    "teamId": list,
}

_STANDINGS_MODIFIERS = {
    "season": str,
    "date": str,
    "record": None,
}


def _internal_modifier_parsing(original_endpoint, internal_modifiers, modifiers={}):
    """Internal function to parse modifier data. Note, modifiers that do not match
    expected types are dropped and no error is raised.

    :param original_endpoint: original endpoint (see endpoints above)
    :param internal_modifiers: dictioanry of acceptable modifiers
    :param modifiers: dictionary of modifiers sent in by the user.
    :return: final endpoint.
    """
    valid_modifiers = []
    
    for key, value in modifiers.items():
        if key in internal_modifiers:
            if internal_modifiers[key] is str and value is not None:
                valid_modifiers.append(f"{key}={value}")
            elif internal_modifiers[key] is list and isinstance(value, str):
                valid_modifiers.append(f"{key}={value}")
            elif internal_modifiers[key] is list and isinstance(value, list):
                matched_types = [isinstance(x, str) for x in value]
                if False in matched_types:
                    break  # break out when a type didn't match
                data_list = ",".join(value)
                valid_modifiers.append(f"{key}={data_list}")
            elif internal_modifiers[key] is None:
                valid_modifiers.append(key)

    if valid_modifiers:
        collapsed = "&".join(valid_modifiers)
        return f"{original_endpoint}?{collapsed}"

    return original_endpoint



def describe_team_endpoint():
    """Gather information about the team endpoint.
    """
    return {
        "roster": "Roster of active players for the specified team.",
        "names": "Roster of active players for the specified team (less descriptive).",
        "next": "Details about the next game.",
        "previous": "Details about the previous game.",
        "stats": "Team stats for the season.",
        "season": "Eight character season information (ex: 20212022).",
        "teamId": "List or string of team ids to query.",
    }


def create_team_endpoint(team_id=None, modifiers={}):
    """Create a full endpoint to retrieve NHL team data from the API. To retrieve a full
    list of modifiers and their uses, please see describe_team_endpoint(). Note that all
    invalid modifiers are skipped, and do Not cause an error.

    :param team_id: When provided, query the api for a single team
    :param modifiers: Dictionary of modifiers to their values. 

    :return: String for the endpoint
    """
    endpoint = API_TEAM_ENDPOINT if team_id is None else f"{API_TEAM_ENDPOINT}/{team_id}"
    return _internal_modifier_parsing(endpoint, _TEAM_MODIFIERS, modifiers)


def describe_standings_endpoint():
    """Gather information about the standings endpoint.
    """
    return {
        "season": "Standings for a specified season.",
        "date": "Standings for a specified date (ex: 2018-01-09).",
        "record": "Detailed information for each team.",
    }


def create_standings_endpoint(modifiers={}):
    """Create a full endpoint to retrieve NHL standings data from the API. To retrieve a full
    list of modifiers and their uses, please see describe_standings_endpoint(). Note that all
    invalid modifiers are skipped, and do Not cause an error.

    :param modifiers: Dictionary of modifiers to their values. 

    :return: String for the endpoint
    """
    return _internal_modifier_parsing(API_STANDINGS_ENDPOINT, _STANDINGS_MODIFIERS, modifiers)


def create_division_endpoint(division_id=None):
    """The division endpoint can either use the base or add an ID.

    :param division_id: When provided, query the api for a single division
    :return: String for the endpoint
    """
    return API_DIVISION_ENDPOINT if division_id is None else f"{API_DIVISION_ENDPOINT}/{division_id}"


def create_conference_endpoint(conference_id=None):
    """The conference endpoint can either use the base or add an ID.

    :param conference_id: When provided, query the api for a single conference
    :return: String for the endpoint
    """
    return API_CONFERENCE_ENDPOINT if conference_id is None else f"{API_CONFERENCE_ENDPOINT}/{conference_id}"


def create_draft_endpoint(year=None):
    """The draft endpoint can either use the base or add a year. If no year
    is added, the current draft year is used.

    :param year: year of the draft
    :return: String for the endpoint
    """
    if isinstance(year, int):
        if year > NHL_FIRST_SEASON and year <= datetime.now().year:
            return f"{API_DRAFT_ENDPOINT}/{year}"

    return API_DRAFT_ENDPOINT


def create_prospects_endpoint(prospect_id=None):
    """The prospect endpoint can either use the base or add an ID.

    :param prospect_id: When provided, query the api for a single prospect
    :return: String for the endpoint
    """
    return API_PROSPECTS_ENDPOINT if prospect_id is None else f"{API_PROSPECTS_ENDPOINT}/{prospect_id}"


def create_awards_endpoint(award_id=None):
    """The award_id endpoint can either use the base or add an ID.

    :param award_id: When provided, query the api for a single award
    :return: String for the endpoint
    """
    return API_AWARDS_ENDPOINT if award_id is None else f"{API_AWARDS_ENDPOINT}/{award_id}"


def create_team_stats_endpoint(team_id):
    """Get the current season stats and current season rankings for a specific team.

    :param team_id: ID of the team to retrieve information about
    :return: String for the endpoint
    """
    return _API_TEAMSTATS_ENDPOINT.format(team_id)


def create_game_endpoint(year, season_type, game):
    '''Create an endpoint that can be used to query the api for a specific game. In
    the event that no data was found from the query the "message" field of json returned
    will contain "Game data couldn't be found".

    :param year: Integer representation of the year in which the game was played
    :param season_type: Integer value for the season type found in the Season Enum
    :param game: Integer value for the game.
    :return: string endpoint for a game
    '''
    return 'http://statsapi.web.nhl.com/api/v1/game/{}{}{}/feed/live'.format(
        year, str(season_type.value).zfill(2), str(game).zfill(4)
    )


class Season(Enum):
    '''The API consists of 4 types of games included in this enum. The
    value from the enum should be zero padded and provided to the api
    when querying for games.
    '''
    PRESEASON = 1
    REGULAR = 2
    PLAYOFFS = 3
    ALLSTAR = 4



