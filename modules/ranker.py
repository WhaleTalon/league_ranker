"""ranker.py module

This module defines the Ranker class that creates and maintains a list of teams
and provides a league ranking list.

"""

from .team import Team

class Ranker:
    """Class to create and maintain a list of teams and provide a league 
    ranking list."""

    # Class constants to support points calculation
    PointsForDraw = 1
    PointsForWin = 3
    PointsForLoss = 0

    def __init__(self) -> None:
        """Initializes an empty list of Team instances that will grow as 
        as game results are processed"""

        self.teams = []

    def getPointsEarned(self, this_team_score: int, 
                        other_team_score: int) -> int:
        """Computes points earned by a team based on a game result."""

        if this_team_score > other_team_score:
            return self.PointsForWin
        elif this_team_score < other_team_score:
            return self.PointsForLoss
        else:
            return self.PointsForDraw

    def getTeam(self, team_name: str) -> Team:
        """Finds and returns an instance of a Team in the teams list. If the
        requested team is not found, a new Team is instantiated and appended
        to the teams list"""

        for team in self.teams:
            if team.name == team_name: return team

        new_team: Team = Team(team_name)
        self.teams.append(new_team)

        return new_team

    def addTeamPoints(self, team_name: str, points_earned: int) -> None:
        """Obtain an instance of a team and increments its points with
        points_earned."""

        team: Team = self.getTeam(team_name)
        team.points += points_earned

    def addGameResults(self, team1_name: str, team1_score: int, 
                        team2_name: str, team2_score: int) -> None:
        """Allocates the points earned by each team based on a game's 
        result"""

        team1_points: int = self.getPointsEarned(team1_score, team2_score)
        self.addTeamPoints(team1_name, team1_points)

        team2_points: int = self.getPointsEarned(team2_score, team1_score)
        self.addTeamPoints(team2_name, team2_points)

    def processGameResultsString(self, game_results: str) -> None:
        """Parses a string representing a game's result. Calls the 
        addGameResults method to process game results if successful,
        else raises a ValueError exception."""

        comma_count: int = game_results.count(",")
        if comma_count == 0: 
            raise ValueError("INVALID ENTRY: Game result must be a comma delimited string of team scores.")
        elif comma_count > 1:
            raise ValueError(f"INVALID ENTRY: Too many comma delimited sections in game results (expected 1, got {comma_count}).")
        
        team1_result, *other, team2_result = game_results.split(",")
        
        team1_result = team1_result.strip().split(" ")
        if not team1_result or len(team1_result) < 2: 
            raise ValueError("INVALID ENTRY: Team 1 score not retrievable from game results.")

        team1_name: str = " ".join(team1_result[:-1])
        if not team1_name: raise ValueError("INVALID ENTRY: Team 1 name not retrievable from game results.")
        team1_score: str  = team1_result[-1]
        if team1_score.isdigit(): 
            team1_score: int = int(team1_score)
        else:
            raise ValueError("INVALID ENTRY: Team 1 score is not an integer.")

        team2_result = team2_result.strip().split(" ")
        if not team2_result or len(team2_result) < 2: 
            raise ValueError("INVALID ENTRY: Team 2 score not retrievable from game results.")

        team2_name: str = " ".join(team2_result[:-1])
        if not team2_name: raise ValueError("INVALID ENTRY: Team 2 name not retrievable from game results.")
        team2_score: str = team2_result[-1]
        if team2_score.isdigit(): 
            team2_score: int = int(team2_score)
        else:
            raise ValueError("INVALID ENTRY: Team 2 score is not an integer.")

        self.addGameResults(team1_name, team1_score, team2_name, team2_score)

    def getRankingList(self) -> list[ Team ]:
        """Calculates the rank of teams in the internal collection, and
        returns a new list of teams sorted according to rank (and 
        alphabetically second)"""

        # List to be compiled, sorted and returned
        ranking_list = []

        # Return an empty list if no teams are found, else prime the list with 
        # the first team from the internal collection
        if len(self.teams) == 0:
            return ranking_list
        else:
            ranking_list.append(self.teams[0])

        # Sequentially evaluate and add teams from the internal collection
        for team in self.teams[1:]:
            for index, tm in enumerate(ranking_list):
                # Add teams in descending points order first, and 
                # alphabetically second
                if team.points > tm.points or (team.points == tm.points and team.name < tm.name):
                    ranking_list.insert(index, team)
                    break

                # Append a team to the end of the list if its points is lower
                # than all the teams already added
                elif index == len(ranking_list)-1:
                    ranking_list.append(team)
                    break
                    
        # Calculate and update the rank of each team in the list
        prev_team: Team = ranking_list[0]
        prev_team.rank = 1
        current_rank: int = 1
        for team in ranking_list[1:]:
            current_rank += 1
            team.rank = prev_team.rank if (team.points == prev_team.points) else current_rank
            prev_team = team

        return ranking_list

    def getRankingListStrings(self) -> list[str]:
        """Obtains the current ranking list, and returns it as a formatted 
        list of strings"""

        ranking_list = self.getRankingList()

        if not ranking_list:
            return ["There are no teams to rank"]
        else:
            string_list: list[str] = [f"{team.rank}. {team.name}, {team.points} pts" for team in ranking_list]
            return string_list

    def __str__(self) -> str:
        """Returns a string representation of this instance and the teams it
        contains."""

        descriptive_string: str = f"Ranker object with {len(self.teams)} teams:\n"
        for index, team in enumerate(self.teams, start = 1):
            descriptive_string += f"{index}. Team {team.name} with {team.points} pts.\n"

        return descriptive_string