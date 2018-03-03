"""
Methods and classes for c++ type comments

Things to note:
Comments inside of strings should not be translated to python equivalents
for example:
    "/* Hello There! */"
    That is a string literal, it should not be turned into a python comment
    if it was the meaning of the code could change to
    "# Hello There!"
    which is bad

    Also if a comment is in the middle of a line we need to wrap the python
    code into a parenthesis block

    myvar = 6 /* Because there are 6 apples */ + 4 /* There are 4 grapes */;
    turns into python
    myvar = (6 # Because there are 6 apples
             + 4 # There are 4 grapes
             )

    while

    myvar = 6 /* Because there are 6 apples */ + 4 /* There are 4 grapes */;

    will turn into

    myvar = (6 # Because there are 6 apples
             + 4) # There are 4 grapes

    comments that come before assignment turn into comments on the preceeding
    line and are joined... there cannot be inline comments in python but this
    should be a good enough equivalent. Observe

    myvar /* Please change this variable name, it is bad */ = 6 + 4;

    turns into 

    # Please change this variable name, it is bad
    myvar = 6 + 4
"""

import abc
import re
from typing import Dict, Optional

from transpile import abstract


class CppBaseComment(abstract.AbstractComment):
    """
    General form of a cpp comment
    """

    def __init__(self, source_text: str,
                 preserve_whitespace: Optional[bool] = False,
                 docstring: Optional[bool] = False,
                 pre_whitespace: Optional[bool] = False,
                 post_whitespace: Optional[bool] = False):

        super().__init__(source_text, preserve_whitespace, docstring)

        self.pre_whitespace = pre_whitespace
        self.post_whitespace = post_whitespace

    @property
    def is_valid(self):
        """
        For the cpp options we just use the REGEX property
        """

        return bool(re.fullmatch(self.REGEX, self.source_text))

    @property
    def py_text(self):
        """
        The python text that should be printed in the module
        """

        return re.sub(self.REGEX, self.REPLACE_PATTERN, self.source_text)


class CppSingleLineComment(CppBaseComment):
    """
    A single line comment in cpp, starting with //

    Cannot be part of a string literal
    """

    SEARCH_PATTERN = (r'(?://)(?P<sl_comment_body>.*((?=\\)[ \t]*\n.*)*)'
                      r'(?=([^"\\]*(\\.|"([^"\\]*\\.)*[^"\\]*"))*[^"]*\n)')

    # Last line of the search pattern; don't include quoted text

    REGEX = re.compile(SEARCH_PATTERN)

    docstring = False

    @classmethod
    def REPLACE(cls, match: object) -> str:
        """
        The function to be used for repl in re.sub
        """

        return (('"""\n' + match.group('sl_comment_body') + '\n"""')
                if cls.docstring else
                ("# " +
                 "\n# ".join((match.group('sl_comment_body') if
                              match.group('sl_comment_body') else
                              "").splitlines())))


class CppMultiLineComment(CppBaseComment):
    """
    A multiline comment, starting with /* and ending with */
    """

    SEARCH_PATTERN = (r'/\*(?P<ml_comment_body>((?!\*/).)*)\*/'
                      r'(?=([^"\\]*(\\.|"([^"\\]*\\.)*[^"\\]*"))*[^"]*$)')

    REGEX = re.compile(SEARCH_PATTERN, re.DOTALL)

    docstring = False

    def __init__(self, source_text: str,
                 preserve_whitespace: Optional[bool] = False,
                 docstring: Optional[bool] = False,
                 pre_whitespace: Optional[bool] = False,
                 post_whitespace: Optional[bool] = False,
                 preserve_line_whitespace: Optional[bool] = False,
                 pre_line_whitespace: Optional[bool] = False,
                 post_line_whitespace: Optional[bool] = False):

        super().__init__(source_text, preserve_whitespace, docstring,
                         pre_whitespace, post_whitespace)

        self.preserve_line_whitespace = preserve_line_whitespace
        self.pre_line_whitespace = pre_line_whitespace
        self.post_line_whitespace = post_line_whitespace

    @classmethod
    def REPLACE(cls, match) -> str:
        """
        The method repl to be used in re.sub()
        """

        return (('"""\n' + match.group('ml_comment_body') + '\n"""')
                if cls.docstring else
                '# ' + '\n# '.join(match.group('ml_comment_body').splitlines()))


class CppCommentGroup(CppMultiLineComment):
    """
    A collection of c++ type comments which are grouped together
    """

    SEARCH_PATTERN = (r'(?P<comment_group>('
                      r'(?P<multiline>'
                      + CppMultiLineComment.SEARCH_PATTERN +
                      r')'
                      r'|(?P<whitespace>\s*)|'
                      r'(?P<singleline>'
                      + CppSingleLineComment.SEARCH_PATTERN +
                      r'))+)')

    REGEX = re.compile(SEARCH_PATTERN)

    @classmethod
    def REPLACE(cls, match: object) -> str:
        """
        The replacement pattern for the comment group
        """

        return (('"""\n' + '\n"""')
                if cls.docstring else
                ("# " + "\n# ".join([])))
