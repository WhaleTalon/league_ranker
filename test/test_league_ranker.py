from cgi import test
import os
import unittest
from unittest.mock import patch, mock_open
from io import StringIO

from modules.ranker import Ranker
import league_ranker as lr

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.test_input_file = os.path.join("test", "test_data.txt")
        self.ranker = Ranker()

    def test_processInputFile(self):
        lr.processInputFile(self.test_input_file, self.ranker)
        results = [("Tarantulas", 6), ("Lions", 5), ("FC Awesome", 1), ("Snakes", 1), ("Grouches", 0)]

        for result in results:
            team = self.ranker.getTeam(result[0])
            self.assertEqual(team.points, result[1],f"processInputFile did not process test input file '{self.test_input_file}' correctly. Team '{result[0]}' given {team.points} pts, should be {result[1]}")

    def test_processCommandlineInput(self):
        with patch("builtins.input", side_effect=["Team1 10, Team2 20", ""]),\
            patch("sys.stdout", new=StringIO()):
            
            lr.processCommandlineInput(self.ranker)

        team1 = self.ranker.getTeam("Team1")
        error_msg = f"processCommandlineInput processed input incorrectly. "
        error_msg += f"Input='team1 10, team2 20', but team1.points="
        error_msg += f"{team1.points} expected {self.ranker.PointsForLoss}"
        self.assertEqual(team1.points, self.ranker.PointsForLoss, error_msg)

        team2 = self.ranker.getTeam("Team2")
        error_msg = f"processCommandlineInput processed input incorrectly."
        error_msg += f" Input='team1 10, team2 20', but team2.points="
        error_msg += f"{team2.points} expected {self.ranker.PointsForWin}"
        self.assertEqual(team2.points, self.ranker.PointsForWin, error_msg)
        

    def test_outputToFile(self):
        mocked_open = mock_open()
        with patch("league_ranker.open", mocked_open, create=True):
            lr.outputToFile(self.ranker, "test_output.txt")

        test_str = "There are no teams to rank"
        mocked_open.assert_called_once_with("test_output.txt", "w")
        mocked_open.return_value.writelines.assert_called_once_with(test_str)

    def test_outputToCommandline(self):
        self.ranker.addTeamPoints("Test_team", 5)

        mock_cmdline = StringIO()
        with patch("sys.stdout", new=mock_cmdline):
            lr.outputToCommandline(self.ranker)

        error_msg = "outputToCommandline printed incorrect ranking list"

        mock_cmdline.seek(0)
        ranking_strings = mock_cmdline.read()
        self.assertIn("1. Test_team, 5 pts", ranking_strings, error_msg)

    def test_main(self):
        mock_cmdline = StringIO()

        with patch("builtins.input", side_effect=["Team1 10, Team2 20", ""]),\
            patch("sys.stdout", new=mock_cmdline):
            
            lr.main([""])

        error_msg = "main function printed incorrect ranking list"

        mock_cmdline.seek(0)
        ranking_strings = mock_cmdline.read()
        self.assertIn("1. Team2, 3 pts", ranking_strings, error_msg)

if __name__ == "__main__":
    unittest.main()