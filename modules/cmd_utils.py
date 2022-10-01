"""cmd_utils.py module

This module provides the following:
1.  Reads application configuration settings in the config.json file and
    instanciates a JSON object.
2.  Defines Modes enumeration to control program logic.
3.  Provides helper functions to write to the command line console.
4.  Functions to obtain, process and output data to/from the command line
    console.
"""

import os
import json
from enum import Enum
from typing import Optional

# Create configuration object from JSON file
with open(os.path.join("modules", "config.json"), "r") as f:
    config = json.load(f)


class Modes(Enum):
    FILE_IO = 1
    COMMAND_LINE_ONLY = 2
    COMMAND_LINE_FILEOUT = 3


def printHelpString() -> None:
    """"Defines application help string and prints it to the command line 
    console"""

    help_string = """
LEAGUE RANKER APPLICATION

Purpose:
Calculates the ranking table for a league.

Usage:
python league_ranker.py [-h|--help]
python league_ranker.py <input_filepath> [<output_path_or_file>]
python league_ranker.py [-o <output_path_or_file>]

Options:
    -h, --help                  Displays this help message.

    input_filepath              Identifies input filepath or file location.

    output_path_or_file         Optional output filename or file location.

    -o                          Command line parser is used to input game 
                                results, but ranking table is sent to a file. 

    When no options or arguments are provided, the command line parser is used
    to input game results, and the ranking table is also printed to the console. 
"""

    print(help_string)


def printDivider() -> None:
    """Prints a divider 'line' consisting of asterisks to the console."""

    print("\n" + "*" * 75 + "\n")


def handleError(ErrorMessage: str, exit: bool = True) -> None:
    """Prints an error message to the console and optionally exits the 
    application."""

    printDivider()
    print("FAILURE:\nThe following exception has occured.")
    print(ErrorMessage)
    printDivider()
    
    if exit:
        printHelpString()
        printDivider()
        quit()


def handleWarning(WarningMessage: str, prompt_to_exit: bool = True) -> None:
    """Prints a warning message to the console and optionally prompts the user 
    to exist the application."""

    printDivider()
    print("WARNING:\n" + WarningMessage + "\n")
    
    while prompt_to_exit:
        opt = input("Do you wish to exit (y/n) ?")
        if opt.lower() == "y":
            quit()
        elif opt.lower() == "n":
            break


def parsePath(filepath: str) -> tuple[str, str, str]:
    """Splits a file path into path location, basename and extension parts."""

    try:
        basepath_without_extension, ext = os.path.splitext(filepath)
        dirname, basename = os.path.split(basepath_without_extension)
        return dirname, basename, ext

    except Exception as Err:
        handleError(Err)


def validateInputFile(input_file: str) -> str:
    """Validates the existence of an input file, and checks if it is a valid
    file format."""

    if not os.path.exists(input_file):
        raise Exception(f"Input path '{input_file}' does not exist.")

    _, _, input_extension = parsePath(input_file)
    if input_extension not in config["valid_file_extensions"]: 
        i_string = input_extension if input_extension else "empty string"
        i_string = f"Invalid extension '{i_string}' found.\n"
        i_string += f"Valid extensions are {config['valid_file_extensions']}"
        raise Exception(i_string)

    return input_file


def validateOutputFile(output_file: str) -> str:
    """Checks if an output filename is provided and well formed, else it 
    provides default file parts. Warns if the file is existing."""

    if not output_file in (None, ""):
        output_dir, output_filename, output_ext = parsePath(output_file)

        if output_dir is None: 
            output_dir = config["default_output_path"]

        if output_filename in (None, ""): 
            output_filename = config["default_output_filename"]
            output_ext = config["default_output_extension"]
        elif output_ext not in config["valid_file_extensions"]: 
            i_string = output_ext if output_ext != "" else "empty string"
            output_ext = config["default_output_extension"]
            i_string = f"Invalid output file extension '{i_string}' found.\n"
            i_string += f"Valid extensions are {config['valid_file_extensions']}.\n"
            i_string += f"Defaulting to extension '{output_ext}'"
            handleWarning(i_string)
            
    else:
        output_dir, output_filename, output_ext = \
            config["default_output_path"], config["default_output_filename"], config["default_output_extension"]

    output_file = os.path.join(output_dir, output_filename + output_ext)
    if os.path.exists(output_file):
        handleWarning(f"Output file '{output_file}' exists. It will be overwritten")

    return output_file


def parseArguments(args: list[str]) -> dict[Modes, Optional[str], Optional[str]]:
    """Parses the command line arguments and determines the correct program
    logic (mode) to apply, and also resolves input/output files if required"""
    
    try:
        # if no arguments supplied, then proceed using command line only
        if not args or (not args[0] and not args[1:]):
            return {"Mode": Modes.COMMAND_LINE_ONLY}
        
        # if help string requested, display it and exit application
        if args[0] == "-h" or args[0] == "--help":
            printHelpString()
            quit()

        if args[0] == "-o":
            # proceed using command line for input, but send output to file
            _, *output_file = args

            if len(output_file) > 1:
                handleWarning(f"Too many arguments received. Discarding: {output_file[:-1]}") 

            output_file = output_file[-1] if len(output_file) > 0 else None
            
            output_file = validateOutputFile(output_file)

            return {"Mode": Modes.COMMAND_LINE_FILEOUT, "Output_file": output_file}
        else:
            # proceed using files for input and output
            input_file, *output_file = args

            if len(output_file) > 1:
                handleWarning(f"Too many arguments received. Discarding: {output_file[:-1]}") 

            output_file = output_file[-1] if len(output_file) > 0 else None

            input_file = validateInputFile(input_file)
            output_file = validateOutputFile(output_file)

            return {"Mode": Modes.FILE_IO, "Input_file": input_file, "Output_file": output_file}

    except Exception as Err:
        handleError(Err)
