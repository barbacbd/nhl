from json import loads
import argparse
from nhl.team import Team
from nhl.player import Player
from nhl.plays import Play


def main():
    """
    
    """
    parser = argparse.ArgumentParser('Script to parse a json encoded file.')
    parser.add_argument(
        '-d', '--directory',
        type=str,
        help='Directory containing all of the json files to parse. [Default=None]',
        default=None
    )
    parser.add_argument(
        '-f', '--filename',
        type=str,
        help='Name of the file to parse. Only used when --directory is None',
        default=None
    )

    args = parser.parse_args()

    files = []
    if args.directory is not None:
        for root, dirs, files in walk(args.directory):
            for file in files:
                if file.endswith(".json"):
                    files.append(file)
    else:
        if args.filename is not None:
            files.append(args.filename)

    if not files:
        raise RuntimeError("No files found")

    # can we batch this ... ?
    for file in files:

        # parse the data in the json file
        with open(file, 'r') as json_file:
            json_data = loads(json_file.read())

        teams = {}
        players = {}
        plays = []

        if json_data:
            if "gameData" in json_data:
                if "teams" in json_data["gameData"]:
                    teams["home"] = Team(json_data["gameData"]["teams"]["home"])
                    teams["away"] = Team(json_data["gameData"]["teams"]["away"])
                
                if "players" in json_data["gameData"]:
                    for player_id, player_data in json_data["gameData"]["players"].items():
                        players[player_id] = Player(player_data)

            if "liveData" in json_data:
                if "plays" in json_data["liveData"]:
                    if "allPlays" in json_data["liveData"]["plays"]:
                        for play in json_data["liveData"]["plays"]["allPlays"]:
                            plays.append(Play(play))
        
        
                
        break  # remove this
    

if __name__ == '__main__':
    main()
