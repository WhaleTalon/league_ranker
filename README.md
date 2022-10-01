# LEAGUE RANKER APPLICATION
## DESCRIPTION

This application computes the ranking table for a League, based on a set of 
game results.

The user can enter game results from the command line, or load a file 
containing the game results.

A ranking table can be viewed via the command line, or output to a file.

Default output file location or filename is taken from the configuration file 
(config.json) if not provided by the user.

## HOW TO RUN THE SCRIPT
### Usage from command line in application root:
python league_ranker.py [-h|--help]

python league_ranker.py <input_filepath> [<output_path_or_file>]

python league_ranker.py [-o <output_path_or_file>]

### Options:
-h, --help &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Displays this help message.

input_filepath &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Identifies input filepath or file location.
     
output_path_or_file &nbsp; &nbsp; Optional output filename or file location.
      
-o &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Command line parser is used to input game 
                              results, but ranking table is sent to a file.
                                      

When no options or arguments are provided, the command line parser is used
to input game results, and the ranking table is also printed to the console.

## HOW TO RUN THE TESTS
### Usage from command line in application root:
python -m unittest discover

## PLATFORM SUPPORT

This application was developed and tested on Windows 10.

It was developed with unix-like environments in mind. However, this has not been tested.
