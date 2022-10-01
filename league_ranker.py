"""League Ranker Application

This application computes the ranking table for a League, based on a set of 
game results.

The user can enter game results from the command line, or load a file 
containing the game results.

A ranking table can be viewed via the command line, or output to a file.

Default output file location or filename is used from the configuration file 
(config.json) if not provided by the user.
"""

import sys

from modules.cmd_utils import parseArguments, handleError, Modes, printDivider
from modules.ranker import Ranker


def processInputFile(filename: str, ranker: Ranker) -> None:
    """Game results are read line-by-line from a file and processed by an 
    instance of the Ranker class."""

    try:
        with open(filename, "r") as f:
            for game_results in f:
                ranker.processGameResultsString(game_results)

    except Exception as Err:
        handleError(Err)


def processCommandlineInput(ranker: Ranker) -> None:
    """Game results are read line-by-line from the command prompt and 
    processed by an instance of the Ranker class."""

    # Provide instructions to user how to use command line interface
    printDivider()
    i_string = "Enter game results in the format: "
    i_string += "<team1_name> <team1_score>, <team2_name> <team2_score>\n"
    i_string += "Press enter to exit\n"
    print(i_string)

    # Read and process game results
    while True:
        try:
            game_results = input("Enter game result: ")
            if game_results == "":
                break
            elif game_results:
                ranker.processGameResultsString(game_results)

        except ValueError as VErr:
            print(VErr)

        except KeyboardInterrupt:
            break

        except Exception as Err:
            handleError(Err)


def outputToFile(ranker: Ranker, output_file: str) -> None:
    """Game results are obtained from an instance of the Ranker class and 
    output to a file. The file is overwritten if it exists."""

    try:
        with open(output_file, "w") as f:
            lines = "\n".join(ranker.getRankingListStrings())
            f.writelines(lines)

    except Exception as Err:
        handleError(Err)


def outputToCommandline(ranker: Ranker) -> None:
    """Game results are obtained from an instance of the Ranker class and 
    output to the command line console."""

    lines = ranker.getRankingListStrings()
    lines.insert(0, "League Ranking Table:")
    printDivider()
    print(*lines, sep="\n", end="\n")
    printDivider()


def main(args) -> None:
    """This function is responsible for start-to-end program flow: parsing
    arguments, obtain and process game results and finally output the ranking
    table."""

    program_options = parseArguments(args)

    ranker = Ranker()
    
    # Input game results
    if program_options["Mode"] == Modes.FILE_IO:
        processInputFile(program_options["Input_file"], ranker)
    else:
        processCommandlineInput(ranker)

    # Output the ranking table
    if program_options["Mode"] == Modes.COMMAND_LINE_ONLY:
        outputToCommandline(ranker)
    else:
        outputToFile(ranker, program_options["Output_file"])


if __name__ == "__main__":
    main(sys.argv[1:])
    