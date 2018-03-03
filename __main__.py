"""
Main and testing functions
"""

import argparse
import re

import coloredlogs
import cpp

PARSER = argparse.ArgumentParser(description='A Python c++ transpiler')

PARSER.add_argument('input', nargs="+", help='The file(s) to parse')

PARSER.add_argument('--test', choices=["comments"],
                    help='Test various functionality')

ARGS = PARSER.parse_args()

if ARGS.test == "comments":

    for file_name in ARGS.input:

        with open(file_name) as test_file:

            test_text = test_file.read()

            #for match in re.finditer(cpp.comments.CppMultiLineComment.REGEX,
            #                         test_text):

            #    print(match.group(0))

            #for match in re.finditer(cpp.comments.CppSingleLineComment.REGEX,
            #                         test_text):

            #    print(match.group(0))

            print(re.sub(cpp.comments.CppMultiLineComment.REGEX,
                         cpp.comments.CppMultiLineComment.REPLACE,
                         re.sub(cpp.comments.CppSingleLineComment.REGEX,
                         cpp.comments.CppSingleLineComment.REPLACE,
                         test_text)))
