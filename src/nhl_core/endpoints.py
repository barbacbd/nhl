from enum import Enum
from datetime import datetime


# The first season of the NHL was 1917 but some teams played in leagues prior to the
# formation of the NHL.
NHL_FIRST_SEASON = 1917

# Initializing the number of games during the regular season to number of teams * 41
# due to 41 home games. This value can and should be overwritten as more teams enter
# the league or the season length changes.
MAX_GAME_NUMBER = 1312


class Season(Enum):
    '''The API consists of 4 types of games included in this enum. The
    value from the enum should be zero padded and provided to the api
    when querying for games.
    '''
    PRESEASON = 1
    REGULAR = 2
    PLAYOFFS = 3
    ALLSTAR = 4


class GameEndpointType(Enum):
    LIVE = 1
    BOXSCORE = 2
    CONTENT = 3


# 
# Base Endpoints
#
API_TEAM_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/teams"
API_DIVISION_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/divisions"
API_CONFERENCE_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/conferences"

API_SCHEDULE_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/schedule"
API_STANDINGS_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/standings"
API_STANDINGTYPES_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/standingsTypes"
API_STATTYPES_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/statTypes"
_API_TEAMSTATS_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/teams/{}/stats"
API_DRAFT_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/draft"
API_PROSPECTS_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/prospects"
API_AWARDS_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/awards"
_API_GAME_ENDPOINT = "http://statsapi.web.nhl.com/api/v1/game/{}/feed/{}"
_API_PEOPLE_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/people/{}"
_API_PEOPLE_STATS_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/people/{}/stats"


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

_SCHEDULE_MODIFIERS = {
    "broadcasts": None,
    "linescore": None,
    "ticket": None,
    "teamId": int,
    "date": str,
    "startDate": str,
    "endDate": str
}

_GAME_MODIFIERS = {
    "diffPatch": None,
    "startTimecode": str,
}

_PEOPLE_STATS_MODIFIERS = {
    "statsSingleSeason": None,
    "season": str,
    "homeAndAway": None,
    "winLoss": None,
    "byMonth": None,
    "byDayOfWeek": None,
    "vsDivision": None,
    "vsConference": None,
    "vsTeam": None,
    "gameLog": None,
    "regularSeasonStatRankings": None,
    "goalsByGameSituation": None,
    "onPaceRegularSeason": None,
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


def describe_schedule_endpoint():
    """Gather information about the schedule endpoint.
    """
    return {
        "broadcasts": "Show the broadcasts of the game.",
        "linescore": "Linescore for completed games.",
        "ticket": "Provides the different places to buy tickets for the upcoming games.",
        "teamId": "Limit results to a specific team.",
        "date": "Single defined date for the search.",
        "startDate": "Start date of the search.",
        "endDate": "End date of the search."
    }

def create_schedule_endpoint(modifiers={}):
    """Create a full endpoint to retrieve NHL schedule data from the API. To retrieve a full
    list of modifiers and their uses, please see describe_schedule_endpoint(). Note that all
    invalid modifiers are skipped, and do Not cause an error.

    :param modifiers: Dictionary of modifiers to their values. 

    :return: String for the endpoint
    """
    return _internal_modifier_parsing(API_SCHEDULE_ENDPOINT, _SCHEDULE_MODIFIERS, modifiers)


def describe_people_stats_endpoint():
    """Gather information about the people (with stats) endpoint.
    """
    return {
        "statsSingleSeason": "Obtains single season statistics for a player.",
        "season": "Eight number season for the data to be applied (ex: 20212022). This is forced for all stats endpoints.",
        "homeAndAway": "Provides a split between home and away games.",
        "winLoss": "Provides the W/L/OT split instead of Home and Away",
        "byMonth": "Monthly split of stats.",
        "byDayOfWeek": "Split done by day of the week.",
        "vsDivision": "Division stats split.",
        "vsConference": "Conference stats split.",
        "vsTeam": "Team stats split.",
        "gameLog": "Provides a game log showing stats for each game of a season.",
        "regularSeasonStatRankings": "Split of this player vs rest of the league.",
        "goalsByGameSituation": "Shows number on when goals for a player occurred.",
        "onPaceRegularSeason": "Projected totals (only valid for current season).",
    }


def create_people_endpoint(people_id, stats=False, modifiers={}):
    """Create a full endpoint to retrieve NHL people data from the API. To retrieve a full
    list of modifiers and their uses, please see describe_people_stats_endpoint(). Note that all
    invalid modifiers are skipped, and do Not cause an error.

    :param people_id: id of the NHL player. 
    :param stats: Boolean value whether player stats are requested or base player data. Stats
    include modifiers to break down information (see describe_people_stats_endpoint()).
    :param modifiers: Dictionary of modifiers to their values. 

    :return: String for the endpoint
    """
    if not stats:
        return _API_PEOPLE_ENDPOINT.format(people_id)
    
    if modifiers:
        if "season" not in modifiers:
            # season may be required at this time
            return None
        elif "season" in modifiers and len(modifiers) != 2: 
            # No other day can be combined
            return None

    return _internal_modifier_parsing(_API_PEOPLE_STATS_ENDPOINT.format(people_id), _PEOPLE_STATS_MODIFIERS, modifiers)


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


def describe_game_endpoint():
    """Gather information about the game endpoint.
    """
    return {
        "diffPatch": "Returns the differences since the startTimeCode (must be combined with startTimeCode).",
        "startTimecode": "Gets the difference since this time (format = yyyymmdd_hhmmss)",
    }


def create_game_endpoint(year, season_type, game, endpoint_type=GameEndpointType.LIVE, modifiers={}):
    '''Create an endpoint that can be used to query the api for a specific game. In
    the event that no data was found from the query the "message" field of json returned
    will contain "Game data couldn't be found". For a full list of modifiers run
    describe_game_endpoint().

    According to documentation found here https://github.com/dword4/nhlapi:
    
    The first 4 digits identify the season of the game (ie. 2017 for the 2017-2018 season). 
    The next 2 digits give the type of game, where 01 = preseason, 02 = regular season, 
    03 = playoffs, 04 = all-star. The final 4 digits identify the specific game number. For 
    regular season and preseason games, this ranges from 0001 to the number of games played.
    (1271 for seasons with 31 teams (2017 and onwards) and 1230 for seasons with 30 teams). 
    For playoff games, the 2nd digit of the specific number gives the round of the playoffs, 
    the 3rd digit specifies the matchup, and the 4th digit specifies the game (out of 7).

    :param year: Integer representation of the year in which the game was played
    :param season_type: Integer value for the season type found in the Season Enum
    :param game: Integer value for the game.
    :param endpoint_type: Type of game data to retrieve (see GameEndpointType above).
    :param modifiers: Dictionary of modifiers to their values. 

    :return: string endpoint for a game
    '''
    st = season_type.value if isinstance(season_type, Enum) else season_type
    game_id = "{}{}{}".format(year, str(st).zfill(2), str(game).zfill(4))
    endpoint = _API_GAME_ENDPOINT.format(game_id, endpoint_type.name.lower())
    return _internal_modifier_parsing(endpoint, _GAME_MODIFIERS, modifiers)

