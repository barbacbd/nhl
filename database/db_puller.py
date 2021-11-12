import argparse
from enum import Enum
from os import mkdir
from os.path import exists, isdir
from datetime import datetime
from requests import get
from json import dumps


NHL_FIRST_SEASON = 1917
MAX_GAME_NUMBER = 1312  # Number of teams * 41 home games


class Season(Enum):
    PRESEASON = 1
    REGULAR = 2
    PLAYOFFS = 3
    ALLSTAR = 4


def _create_url(year, season_type, game_number):
    """
    :param year: Year that the url should be applied to
    :param season_type: int representation of the season type
    :param game_number: int number of the game for the year
    
    :return: string url that should be used to get individual game statistics
    """
    return 'http://statsapi.web.nhl.com/api/v1/game/{}{}{}/feed/live'.format(
        year, str(season_type).zfill(2), str(game_number).zfill(4)
    )



def main():
    """
    Main entry point
    """
    parser = argparse.ArgumentParser('Script to pull nhl data from specific years.')
    parser.add_argument(
        '-y', '--years',
        type=str,
        help='Year that you wish to have the data pulled for. If the user provides `all` then'
             ' all years will be pulled from the start of the NHL',
        default='all'
    )
    parser.add_argument(
        '-s', '--season',
        type=str,
        help='Type of season for which to search the data',
        choices=[x.name for x in Season],
        default=Season.REGULAR.name
    )
    
    args = parser.parse_args()
    
    years = []
    if args.years.lower() == "all":
        # this may grab an extra year, but I am not sure how the nhl database is setup
        years = [x for x in range(1917, int(datetime.now().year))]
    else:
        try:
            years = [int(args.years)]
        except (valueError, TypeError) as e:
            print(e)
            raise
    
    try:
        season_type = [x for x in Season if x.name == args.season][0].value
    except (IndexValue, TypeError) as e:
        print(e)
        raise

    # create all of the json files by pulling the requests from
    # the nhl database
    for year in years:
        if not exists(str(year)):
            mkdir(str(year))
        else:
            if not isdir(str(year)):
                mkdir(str(year))
            
        for i in range(MAX_GAME_NUMBER):
            json_request = get(_create_url(year, season_type, i)).json()

            if "message" in json_request and json_request["message"] == "Game data couldn't be found":
                continue
            
            with open("{}/{}_{}.json".format(year, year, i), "w+") as f:
                f.write(dumps(json_request, indent=4))


if __name__ == "__main__":
    main()
    
