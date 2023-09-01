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



