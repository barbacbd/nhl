from unittest import main, TestCase
from nhl import *
from json import dumps
from os import remove
from os.path import exists, dirname, abspath


class NHLTest(TestCase):
    
    goodData = NotImplemented
    
    @classmethod
    def setUpClass(cls):
        cls.goodData = ParseFromFile(dirname(abspath(__file__)) + "/GoodNHLData.json")

    def test_01_valid_init(self):
        """Read in a valid file and ensure the contents are good
        """
        self.assertTrue(self.goodData is not None)
        self.assertTrue(isinstance(self.goodData, NHLData))
        self.assertTrue(len(self.goodData.children) > 0)

    def test_02_valid_simple_query_list(self):
        """Use a simple list for querying the data. This is using a known value set.
        """
        self.assertTrue(self.goodData.query(["gameData"]) is not None)
    
    def test_03_valid_complex_query_list(self):
        """Use a simple list for querying the data. This is using a known value set.
        """
        self.assertTrue(self.goodData.query(["gameData", "teams", "away", "venue"]) is not None)
    
    def test_04_valid_complex_query_list_aliases(self):
        """Use a simple list for querying the data. This is using a known value set. The value set
            contains aliases of the original text. The aliases are merely all lower cased values.
        """
        self.assertTrue(self.goodData.query(["gamedata", "teams", "away", "venue"]) is not None)
        
    def test_05_valid_simple_query_str(self):
        """Use a simple list for querying the data. This is using a known value set.
        """
        self.assertTrue(self.goodData.query("gameData") is not None)
    
    def test_06_valid_complex_query_str(self):
        """Use a simple list for querying the data. This is using a known value set.
        """
        self.assertTrue(self.goodData.query("gameData.teams.away.venue") is not None)

    def test_07_valid_complex_query_str_alias(self):
        """Use a simple list for querying the data. This is using a known value set. The value set
            contains aliases of the original text. The aliases are merely all lower cased values.
        """
        self.assertTrue(self.goodData.query("gamedata.teams.away.venue") is not None)

    def test_08_invalid_simple_query_list(self):
        """Use a simple list for querying the data. This is using a known value set to be invalid.
        """
        self.assertTrue(self.goodData.query(["badData"]) is None)
    
    def test_09_invalid_complex_query_list(self):
        """Use a simple list for querying the data. This is using a known value set to be invalid.
        """
        self.assertTrue(self.goodData.query(["gameData", "teams", "away", "badData"]) is None)
            
    def test_10_invalid_simple_query_str(self):
        """Use a simple list for querying the data. This is using a known value set to be invalid.
        """
        self.assertTrue(self.goodData.query("badData") is None)
    
    def test_11_invalid_complex_query_str(self):
        """Use a simple list for querying the data. This is using a known value set to be invalid.
        """
        self.assertTrue(self.goodData.query("gameData.teams.away.badData") is None)

    def test_12_valid_json_file_no_data(self):
        """Test a valid json file, but no data in the file.
        """
        filename = "ValidJsonNoData.json"
        
        with open(filename, "w+") as f:
            f.write(dumps({}, indent=4))
        
        data = ParseFromFile(filename)
        
        if exists(filename):
            remove(filename)
        
        self.assertTrue(isinstance(data, NHLData))
        self.assertTrue(len(data.children) == 0)
    
    def test_13_valid_filename_does_not_exist(self):
        """Filename is json ext but does not exist
        """
        filename = "InvalidFilename.json"
        self.assertTrue(ParseFromFile(filename) is None)
    
    def test_14_invalid_filename_does_not_exist(self):
        """Filename is not json ext and does not exist
        """
        filename = "InvalidFilename.yaml"
        self.assertTrue(ParseFromFile(filename) is None)


if __name__ == '__main__':
    main()
