"""
Faculties for parsing cpp styled classes and reproducing them in Python
"""

import re

from transpile import abstract

class CppClass(abstract.AbstractSymbol):
    """
    A cpp class definition
    """
    
    SEARCH_PATTERN = (r'(?=\s*)class\s+')

    REGEX = re.compile(SEARCH_PATTERN)

    @classmethod
    def REPLACE(cls, match: object):
        """
        The replacement pattern for a cpp class definition
        """

        return ()