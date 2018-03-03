"""
C++ style statement parsers

Statements are just code preceeded by a semicolon
"""

import re

import classes
import comments

from transpile import abstract


class CppStatement(abstract.AbstractSymbol):
    """
    A statement in c++, starts after ; and ends before ;
    """

    SEARCH_PATTERN = (r'(?<=;)(?P<statement_body>[^;]*);')

    REGEX = re.compile(SEARCH_PATTERN)

    @classmethod
    def REPLACE(cls, match: object) -> str:
        """
        The repl method to be used in the re.sub function
        """

        statement_body_text = (match.group('statement_body') if
                               match.group('statement_body') else '')

        statement_body_text = re.sub()
