"""team.py module

This module defines the Team class to represent the data about a team.

"""

from dataclasses import dataclass

@dataclass
class Team:
    """Class to represent a team's data"""

    name: str
    points: int = 0
    rank: int = None