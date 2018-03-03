"""
Abstract classes for transpiling to python
"""

import abc
import re
from typing import Optional

class AbstractSymbol(abc.ABC):
    """
    A class that parses something in another language and converts to python
    """

    @property
    @abc.abstractmethod
    def SEARCH_PATTERN(self) -> str:
        """
        The pattern to search for, should be a static class attribute
        """

        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def REPLACE(cls, match: object) -> str:
        """
        The pattern to substitute for, should be a static class attribute
        """

        raise NotImplementedError

    @property
    @abc.abstractmethod
    def REGEX(self) -> object:
        """
        Precompiled regex search pattern, should be a static class attribute
        """

        raise NotImplementedError

    def __init__(self, source_text: str,
                 preserve_whitespace: Optional[bool] = False):

        self.source_text = source_text

        self.preserve_whitespace = preserve_whitespace

    @property
    @abc.abstractmethod
    def is_valid(self) -> bool:
        """
        Returns true if syntax is valid for the source language, else false

        Classmethod version
        """

        raise NotImplementedError

    @property
    @abc.abstractmethod
    def py_text(self) -> str:
        """
        Returns the Python version of the symbol
        """

        raise NotImplementedError

class AbstractComment(AbstractSymbol):
    """
    A symbol that should be converted into a python comment

    If docstring is True, format the comment as if it were a docstring
    """

    def __init__(self, source_text: str, 
                 preserve_whitespace: Optional[bool] = False,
                 docstring: Optional[bool] = False):

        super().__init__(source_text, preserve_whitespace)

        self.docstring = docstring

class AbstractClass(AbstractSymbol):
    """
    A class that detects a class defintion in a language and converts to Python
    """

    pass