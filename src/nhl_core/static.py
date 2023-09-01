from enum import Enum


# The first season of the NHL was 1917 but some teams played in leagues prior to the
# formation of the NHL.
NHL_FIRST_SEASON = 1917

# Initializing the number of games during the regular season to number of teams * 41
# due to 41 home games. This value can and should be overwritten as more teams enter
# the league or the season length changes.
MAX_GAME_NUMBER = 1312

# The endpoint provides data about all teams in the NHL
API_TEAM_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/teams"

_TEAM_MODIFIERS = {
    "roster": None,
    "names": None,
    "next": None,
    "previous": None,
    "stats": None,
    "season": str,
    "teamId": list,
}

def describe_team_endpoint():
    """Gather information about the team endpoint.
    """
    return {
        "roster": "roster of active players for the specified team",
        "names": "roster of active players for the specified team (less descriptive)",
        "next": "details about the next game",
        "previous": "details about the previous game",
        "stats": "team stats for the season",
        "season": "eight character season information, ex: 20212022",
        "teamId": "list or string of team ids to query",
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

    valid_modifiers = []
    
    for key, value in modifiers.items():
        if key in _TEAM_MODIFIERS:
            if _TEAM_MODIFIERS[key] is str and value is not None:
                valid_modifiers.append(f"{key}={value}")
            elif _TEAM_MODIFIERS[key] is list and isinstance(value, str):
                valid_modifiers.append(f"{key}={value}")
            elif _TEAM_MODIFIERS[key] is list and isinstance(value, list):
                matched_types = [isinstance(x, str) for x in value]
                if False in matched_types:
                    break  # break out when a type didn't match
                data_list = ",".join(value)
                valid_modifiers.append(f"{key}={data_list}")
            elif _TEAM_MODIFIERS[key] is None:
                valid_modifiers.append(key)

    if valid_modifiers:
        collapsed = "&".join(valid_modifiers)
        return f"{endpoint}?{collapsed}"

    return endpoint


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



