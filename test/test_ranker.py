import unittest
import sys
sys.path.append("..")

from modules.ranker import Ranker

class TestRanker(unittest.TestCase):

    def setUp(self):
        self.ranker = Ranker()
        self.test_team1 = self.ranker.getTeam("Test Team 1")
        self.test_team2 = self.ranker.getTeam("Test Team 2")

    def test_instance_of_ranker(self):
        self.assertIsInstance(self.ranker, Ranker, 
            "Failed to instantiate a Ranker object")

        self.assertTrue(self.ranker.PointsForDraw >= 0, 
            "PointsForDraw not initialized")

        self.assertTrue(self.ranker.PointsForWin >= 0, 
            "PointsForWin not initialized")

        self.assertTrue(self.ranker.PointsForLoss >= 0, 
            "PointsForLoss not initialized")

    def test_getPointsEarned(self):
        self.assertEqual(self.ranker.getPointsEarned(10, 10), 
            self.ranker.PointsForDraw, 
            "getPointsEarned returns incorrect result for a Draw")

        self.assertEqual(self.ranker.getPointsEarned(10, 1), 
            self.ranker.PointsForWin, 
            "getPointsEarned returns incorrect result for a Win")

        self.assertEqual(self.ranker.getPointsEarned(1, 10), 
            self.ranker.PointsForLoss, 
            "getPointsEarned returns incorrect result for a Loss")

    def test_getTeam(self):
        self.assertIn(self.test_team1, self.ranker.teams, 
            "getTeam not appending new teams to the teams collection")

        self.assertEqual(self.ranker.getTeam("Test Team 1"), self.test_team1, 
            "getTeam not finding team in teams collection")

    def test_addTeamPoints(self):
        self.ranker.addTeamPoints("Test Team 2", 5)
        self.assertEqual(self.test_team2.points, 5, 
            "addTeamPoints failed to add points correctly")

        msg = "addTeamPoints failed to add points correctly, "
        msg += "or else failed to create new team"
        self.ranker.addTeamPoints("Test Team 3", 7)
        self.ranker.addTeamPoints("Test Team 3", 3)
        self.assertEqual(self.ranker.getTeam("Test Team 3").points, 10, msg)

    def test_addGameResults(self):
        points = self.ranker.PointsForDraw

        self.ranker.addGameResults("Test Team 1", 10, "Test Team 2", 10)
        self.assertEqual(self.ranker.getTeam("Test Team 1").points, points, 
            "addGameResults fialed to add points correctly for a Draw")

        self.assertEqual(self.ranker.getTeam("Test Team 2").points, points, 
            "addGameResults fialed to add points correctly for a Draw")

        self.ranker.addGameResults("Test Team 1", 1, "Test Team 2", 10)
        self.assertEqual(self.ranker.getTeam("Test Team 1").points, 
            points + self.ranker.PointsForLoss, 
            "addGameResults failed to add points correctly for a Loss")

        self.assertEqual(self.ranker.getTeam("Test Team 2").points, 
            points + self.ranker.PointsForWin, 
            "addGameResults failed to add points correctly for a Win")

    def test_processGameResultsString(self):
        test_strings = [
            ("Test Team 1 10 Test Team 2 10", "INVALID ENTRY: Game result must be a comma delimited string of team scores."),
            ("Test Team 1 10, Test 20, Team 2 10", "INVALID ENTRY: Too many comma delimited sections in game results (expected 1, got 2)."),
            ("Test, Test Team 2 10", "INVALID ENTRY: Team 1 score not retrievable from game results."),
            ("Test Team 1 1a, Test Team 2 10", "INVALID ENTRY: Team 1 score is not an integer."),
            ("Test Team 1 10, Test", "INVALID ENTRY: Team 2 score not retrievable from game results."),
            ("Test Team 1 10, Test Team 2 1d", "INVALID ENTRY: Team 2 score is not an integer.")
        ]

        for t_strings in test_strings:
            with self.assertRaises(ValueError) as err:
                self.ranker.processGameResultsString(t_strings[0])
            self.assertEqual(str(err.exception), t_strings[1])

        test_string = "Test Team 1 10, Test Team 2 10"

        points = self.ranker.PointsForDraw
        self.ranker.processGameResultsString(test_string)
        self.assertEqual(self.ranker.getTeam("Test Team 1").points, points, 
            "processGameResultsString added points incorrectly for a Draw")

        self.assertEqual(self.ranker.getTeam("Test Team 2").points, points, 
            "processGameResultsString added points incorrectly for a Draw")

        test_string = "Test Team 1 10, Test Team 2 20"

        self.ranker.processGameResultsString(test_string)
        self.assertEqual(self.ranker.getTeam("Test Team 1").points, 
            points + self.ranker.PointsForLoss, 
            "processGameResultsString added points incorrectly for a Loss")

        self.assertEqual(self.ranker.getTeam("Test Team 2").points, 
            points + self.ranker.PointsForWin, 
            "processGameResultsString added points incorrectly for a Win")

    def test_getRankingList(self):
        self.ranker.teams.clear()
        self.ranker.addTeamPoints("Arms", 10)
        self.ranker.addTeamPoints("Legs", 8)
        self.ranker.addTeamPoints("Torso", 5)
        self.ranker.addTeamPoints("Chest", 5)
        self.ranker.addTeamPoints("Head", 0)

        Arms = self.ranker.getTeam("Arms")
        Legs = self.ranker.getTeam("Legs")
        Torso = self.ranker.getTeam("Torso")
        Chest = self.ranker.getTeam("Chest")
        Head = self.ranker.getTeam("Head")

        results_list = [Arms, Legs, Chest, Torso, Head]

        self.assertEqual(self.ranker.getRankingList(), results_list, 
            "getRankingList failed to generate correct ranking list")

        results_list = [(Arms, 1), (Legs, 2), (Chest, 3), 
                        (Torso, 3), (Head, 5)]

        for result in results_list:
            self.assertEqual(result[0].rank, result[1], 
                "getRankingList failed to compute correct rank value.")

    def test_getRankingListStrings(self):
        self.ranker.teams.clear()

        self.assertEqual(self.ranker.getRankingListStrings(), 
            ["There are no teams to rank"], 
            "getRankingListStrings failed when there are no teams to rank")

        self.ranker.addTeamPoints("Arms", 10)
        self.ranker.addTeamPoints("Legs", 8)
        self.ranker.addTeamPoints("Torso", 5)
        self.ranker.addTeamPoints("Chest", 5)
        self.ranker.addTeamPoints("Head", 0)

        Arms = self.ranker.getTeam("Arms")
        Legs = self.ranker.getTeam("Legs")
        Torso = self.ranker.getTeam("Torso")
        Chest = self.ranker.getTeam("Chest")
        Head = self.ranker.getTeam("Head")

        results_list = [Arms, Legs, Chest, Torso, Head]

        

        results_list = [(Arms, 1), (Legs, 2), (Chest, 3), 
                        (Torso, 3), (Head, 5)]

        results_list = [
            "1. Arms, 10 pts", "2. Legs, 8 pts", "3. Chest, 5 pts", 
            "3. Torso, 5 pts", "5. Head, 0 pts"
        ]

        self.assertEqual(self.ranker.getRankingListStrings(),  results_list, 
            "getRankingListStrings formed ranking list string incorrectly.")

if __name__ == "__main__":
    unittest.main()