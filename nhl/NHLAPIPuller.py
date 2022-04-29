import argparse
from enum import Enum
from os import mkdir
from os.path import exists, isdir
from datetime import datetime
from requests import get
from json import dumps
from json.decoder import JSONDecodeError
from shutil import rmtree


NHL_FIRST_SEASON = 1917
MAX_GAME_NUMBER = 1312  # Number of teams * 41 home games


class Season(Enum):
    PRESEASON = 1
    REGULAR = 2
    PLAYOFFS = 3
    ALLSTAR = 4


def main():
    """
    Main entry point
    """
    parser = argparse.ArgumentParser('Pull NHL data from the web API based on the following parameters: ')
    parser.add_argument(
        '-g', '--games',
        type=str,
        nargs="+",
        help='Type game for the years that are selected.',
        default=["all"]
    )
    parser.add_argument(
        '-s', '--season',
        type=str,
        help='Type of seasonal games for which the data should be gathered.',
        choices=[x.name for x in Season],
        default=Season.REGULAR.name
    )
    parser.add_argument(
        '-y', '--years',
        type=str,
        nargs="+",
        help='The years of data that is requested.',
        default=["all"]
    )
    parser.add_argument(
        '--dir',
        type=str,
        help='Output directory.',
        default='nhl_data'
    )
    args = parser.parse_args()


    # make this an arg
    if exists(args.dir):
        rmtree(args.dir)
    mkdir(args.dir)
    

    current_year = int(datetime.now().year)

    # adjust the data in years
    years = [x.lower() for x in args.years]

    try:
        season_type = [x for x in Season if x.name == args.season][0].value
    except (IndexError, TypeError) as e:
        print(e)
        raise
    
    if "all" in years:
        # rewrite years
        years = [x for x in range(1917, current_year)]
        
    else:
        years_copy = years.copy()
        years = []

        # find valid years
        for year in years_copy:
            if NHL_FIRST_SEASON <= int(year) <= current_year:
                years.append(int(year))

        # order the years to grab
        years.sort()

    
    # adjust the data in games
    games = [x.lower() for x in args.games]
    if "all" in games:
        games = [i+1 for i in range(MAX_GAME_NUMBER)]
    else:
        games_copy = games.copy()
        games = []

        # find valid games
        for game in games_copy:
            if 1 <= int(game) <= MAX_GAME_NUMBER:
                games.append(int(game))

        # order the games to grab
        games.sort()
        
    # create all of the json files by pulling the requests from
    # the nhl database
    for year in years:
        _dir = "{}/{}".format(args.dir, year)
        mkdir(_dir)

        for game in games:
            try:
                json_request = get(
                    'http://statsapi.web.nhl.com/api/v1/game/{}{}{}/feed/live'.format(
                        year, str(season_type).zfill(2), str(game).zfill(4)
                    )
                ).json()
            except JSONDecodeError as e:
                # searched for a game that didn't exit. this is possible for years that
                # were queried in far in the past
                break

            # failed find, continue on
            if "message" in json_request and json_request["message"] == "Game data couldn't be found":
                continue
            
            with open("{}/{}_{}.json".format(_dir, year, game), "w+") as f:
                f.write(dumps(json_request, indent=4))


if __name__ == "__main__":
    main()
    
