from unittest import main, TestCase
from nhl_core.endpoints import (
    API_TEAM_ENDPOINT, 
    _TEAM_MODIFIERS,
    create_team_endpoint, 
    API_DIVISION_ENDPOINT,
    create_division_endpoint,
    API_CONFERENCE_ENDPOINT,
    create_conference_endpoint,
    API_DRAFT_ENDPOINT,
    create_draft_endpoint,
    API_PROSPECTS_ENDPOINT,
    create_prospects_endpoint,
    API_AWARDS_ENDPOINT,
    create_awards_endpoint,
    _STANDINGS_MODIFIERS,
    API_STANDINGS_ENDPOINT,
    create_standings_endpoint,
    _SCHEDULE_MODIFIERS,
    API_SCHEDULE_ENDPOINT,
    create_schedule_endpoint,
    _API_GAME_ENDPOINT,
    _GAME_MODIFIERS,
    Season,
    GameEndpointType,
    create_game_endpoint,
)
from random import choice, randint
from datetime import datetime


class EndpointTests(TestCase):
    
    def test_01_base_team_endpoint(self):
        assert create_team_endpoint() == API_TEAM_ENDPOINT

    def test_02_team_endpoint_single_team(self):
        team_id = "100"
        endpoint = create_team_endpoint(team_id=team_id)

        assert endpoint.endswith(team_id)

    def test_03_team_endpoint_valid_modifier_none(self):
        random_choice = choice([x for x, y in _TEAM_MODIFIERS.items() if y is None])
        random_type = _TEAM_MODIFIERS[random_choice]
        assert create_team_endpoint(modifiers={random_choice: random_type}).endswith(random_choice)

    def test_04_team_endpoint_valid_modifier_str(self):
        """Test a modifier that requires string
        """
        key = "season"
        currentyear = int(datetime.now().year)
        season = f"{currentyear-2}{currentyear-1}"
        assert create_team_endpoint(modifiers={key: season}).endswith(f"season={season}")

    def test_05_team_endpoint_valid_modifier_str(self):
        """Test a modifier that requires a list or string
        """
        key = "teamId"
        num_teams = randint(1, 4)
        
        team_ids = set()
        for i in range(num_teams):
            team_ids.add(str(randint(1, 50)))
            
        team_ids = list(team_ids)
                
        teams_str = ",".join(team_ids)
        assert create_team_endpoint(modifiers={key: team_ids}).endswith(teams_str)
            
    def test_06_team_endpoint_valid_modifiers(self):
        endpoint = create_team_endpoint(modifiers={"roster": None, "season": "20212022"})
        assert endpoint.endswith("roster&season=20212022")

    def test_07_team_endpoint_valid_modifier_bad_type_ignore_value(self):
        endpoint = create_team_endpoint(modifiers={"roster": "random_data"})
        assert endpoint.endswith("roster")

    def test_08_team_endpoint_valid_modifier_bad_type(self):
        """The types in the list are not a string
        """
        key = "teamId"
        num_teams = randint(1, 4)
        
        team_ids = set()
        for i in range(num_teams):
            team_ids.add(randint(1, 50))
            
        team_ids = list(team_ids)
                
        assert create_team_endpoint(modifiers={key: team_ids}) == API_TEAM_ENDPOINT
    
    def test_08_team_endpoint_invalid_modifier(self):
        """Test an invalid modifier"""
        key = "randomData"
        assert create_team_endpoint(modifiers={key: None}) == API_TEAM_ENDPOINT

    def test_09_team_endpoint_valid_and_invalid_modifiers(self):
        endpoint = create_team_endpoint(modifiers={"roster": None, "badData": None})
        assert endpoint.endswith("roster")
    
    def test_10_base_division_endpoint(self):
        assert create_division_endpoint() == API_DIVISION_ENDPOINT
    
    def test_11_division_endpoint(self):
        assert create_division_endpoint(division_id=3).endswith("3")
    
    def test_13_base_conference_endpoint(self):
        assert create_conference_endpoint() == API_CONFERENCE_ENDPOINT
    
    def test_14_conference_endpoint(self):
        assert create_conference_endpoint(conference_id=2).endswith("2")
    
    def test_15_base_draft_endpoint(self):
        assert create_draft_endpoint() == API_DRAFT_ENDPOINT
    
    def test_16_draft_endpoint(self):
        year = datetime.now().year - 1
        assert create_draft_endpoint(year=year).endswith(str(year))
    
    def test_17_draft_endpoint_too_high(self):
        year = datetime.now().year + 10
        assert create_draft_endpoint(year=year) == API_DRAFT_ENDPOINT

    def test_18_draft_endpoint_too_low(self):
        year = 0
        assert create_draft_endpoint(year=year) == API_DRAFT_ENDPOINT

    def test_19_base_prospects_endpoint(self):
        assert create_prospects_endpoint() == API_PROSPECTS_ENDPOINT
    
    def test_20_prospects_endpoint(self):
        assert create_prospects_endpoint(2).endswith("2")
    
    def test_21_base_awards_endpoint(self):
        assert create_awards_endpoint() == API_AWARDS_ENDPOINT
    
    def test_22_awards_endpoint(self):
        assert create_awards_endpoint(2).endswith("2")
    
    def test_23_base_standings_endpoint(self):
        assert create_standings_endpoint() == API_STANDINGS_ENDPOINT

    def test_24_standings_endpoint_valid_modifier_none(self):
        random_choice = choice([x for x, y in _STANDINGS_MODIFIERS.items() if y is None])
        random_type = _STANDINGS_MODIFIERS[random_choice]
        assert create_standings_endpoint(modifiers={random_choice: random_type}).endswith(random_choice)

    def test_25_standings_endpoint_valid_modifier_str(self):
        """Test a modifier that requires string
        """
        key = "season"
        currentyear = int(datetime.now().year)
        season = f"{currentyear-2}{currentyear-1}"
        assert create_standings_endpoint(modifiers={key: season}).endswith(f"season={season}")
    
    def test_26_schedule_team_endpoint(self):
        assert create_schedule_endpoint() == API_SCHEDULE_ENDPOINT

    def test_27_team_endpoint_valid_modifier_none(self):
        random_choice = choice([x for x, y in _SCHEDULE_MODIFIERS.items() if y is None])
        random_type = _SCHEDULE_MODIFIERS[random_choice]
        assert create_schedule_endpoint(modifiers={random_choice: random_type}).endswith(random_choice)

    def test_28_team_endpoint_valid_modifier_str(self):
        """Test a modifier that requires string
        """
        key = "date"
        dateexample = "2018-01-09"
        assert create_schedule_endpoint(modifiers={key: dateexample}).endswith(f"{key}={dateexample}")

    def test_30_game_endpoint_normal(self):
        """ A base test will include the year, season type and game
        """
        year = "2022"
        season = Season.REGULAR
        game = 1

        # 4 digits - year
        # 2 digits - season type
        # 4 digits - game number

        assert "2022020001" in create_game_endpoint(year, season, game)

    def test_31_game_endpoint_content(self):
        """ A base test will include the year, season type and game. Add the content to the type.
        """
        year = "2022"
        season = Season.REGULAR
        game = 1
        data = GameEndpointType.CONTENT

        # 4 digits - year
        # 2 digits - season type
        # 4 digits - game number
        endpoint = create_game_endpoint(year, season, game, data)
        assert "2022020001" in endpoint
        assert endpoint.endswith(data.name.lower())
    
    def test_32_game_endpoint_modifier(self):
        """ A base test will include the year, season type and game. Add valid modifiers
        """
        year = "2022"
        season = Season.REGULAR
        game = 1
        mods = _GAME_MODIFIERS.copy()
        mods["startTimecode"] = "20221010_183000"

        # 4 digits - year
        # 2 digits - season type
        # 4 digits - game number
        endpoint = create_game_endpoint(year, season, game, modifiers=mods)
        assert "2022020001" in endpoint
        assert endpoint.endswith("startTimecode=20221010_183000")


if __name__ == '__main__':
    main()
