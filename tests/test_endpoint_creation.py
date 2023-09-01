from unittest import main, TestCase
from nhl_core.static import create_team_endpoint, API_TEAM_ENDPOINT, _TEAM_MODIFIERS
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
    


if __name__ == '__main__':
    main()
