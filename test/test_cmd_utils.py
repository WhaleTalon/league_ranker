import os
import sys
sys.path.append("..")
import unittest
from unittest.mock import patch
from io import StringIO

import modules.cmd_utils as utils

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.fake_output_file = os.path.join("test", "somefile.txt")

        self.default_output_file = os.path.join(
            utils.config["default_output_path"], 
            utils.config["default_output_filename"] 
            + utils.config["default_output_extension"])

        self.test_input_file = os.path.join("test", "test_data.txt")

    def test_config(self):
        keys = ("modes", "default_output_path", "default_output_filename",
                "default_output_extension", "valid_file_extensions")

        config_keys = utils.config.keys()
        for key in keys:
            self.assertIn(key, config_keys, 
                f"CONFIG object is missing key '{key}'")

    def test_parsePath(self):
        platform_filename = os.path.join("some_location", "filename.ext")

        self.assertEqual(utils.parsePath(platform_filename), ("some_location", "filename", ".ext"), "parsePath failed to parse correctly")

    def test_validateInputFile(self):
        with self.assertRaises(Exception) as err:
            utils.validateInputFile("file_that_does_not_exist.txt")
            
        with self.assertRaises(Exception) as err:
            utils.validateInputFile(os.path.join("test", "test_file_with_invalid_ext.ext"))

        try:
            utils.validateInputFile(os.path.join("test", "test_data.txt"))
        except Exception:
            self.fail("validateInputFile raised an unexpected exception.")

    def test_validateOutputFile(self):
        self.assertEqual(utils.validateOutputFile(None), 
            self.default_output_file)

        i_string = os.path.join(utils.config["default_output_path"], "")
        self.assertEqual(utils.validateOutputFile(i_string), 
            self.default_output_file)

        i_string = os.path.join("test", "test_file_with_invalid_ext.ext")
        r_string = os.path.join("test", "test_file_with_invalid_ext" \
            + utils.config["default_output_extension"])
        with patch("builtins.input", return_value="n"), \
            patch("sys.stdout", new=StringIO()):
            
            self.assertEqual(utils.validateOutputFile(i_string), r_string)
        
    def test_parseArguments(self):
        self.assertEqual(utils.parseArguments([]), 
            {"Mode": utils.Modes.COMMAND_LINE_ONLY}, 
            "parseArguments failed to return COMMAND_LINE_ONLY mode when no arguments were supplied")

        self.assertEqual(utils.parseArguments([""]), 
            {"Mode": utils.Modes.COMMAND_LINE_ONLY}, 
            "parseArguments failed to return COMMAND_LINE_ONLY mode when no arguments were supplied")
        
        with patch("builtins.input", return_value="n"), \
            patch("sys.stdout", new=StringIO()):

            self.assertEqual(utils.parseArguments(["-o"]), 
                {"Mode": utils.Modes.COMMAND_LINE_FILEOUT, 
                "Output_file": self.default_output_file})

        test_args = ["-o", "extra argument", self.fake_output_file]
        with patch("builtins.input", return_value="n"), \
            patch("sys.stdout", new=StringIO()):

            self.assertEqual(utils.parseArguments(test_args), 
                {"Mode": utils.Modes.COMMAND_LINE_FILEOUT, 
                "Output_file": self.fake_output_file})

        test_args = [self.test_input_file, self.fake_output_file]
        with patch("builtins.input", return_value="n"), \
            patch("sys.stdout", new=StringIO()):

            self.assertEqual(utils.parseArguments(test_args), 
                {"Mode": utils.Modes.FILE_IO, 
                "Input_file": self.test_input_file, 
                "Output_file": self.fake_output_file})

        with patch("builtins.input", return_value="n"), \
            patch("sys.stdout", new=StringIO()):
            
            self.assertEqual(utils.parseArguments([self.test_input_file]), 
                {"Mode": utils.Modes.FILE_IO, 
                "Input_file": self.test_input_file, 
                "Output_file": self.default_output_file})


if __name__ == "__main__":
    unittest.main()