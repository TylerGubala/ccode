"""
Transpilation of c-type code into python
"""

import re
from typing import Iterable, Optional

from ..transpile import abstract

class CppBuildEnvironment():
    """
    Build environment for c plus plus code
    """

    def __init__(self, headers: Optional[Iterable[str]] = None,
                 dlls: Optional[Iterable[str]] = None,
                 sources: Optional[Iterable[str]] = None):

        self.headers = headers if headers is not None else []

        self.dlls = dlls if dlls is not None else []

        self.sources = sources if sources is not None else []

    def build(self) -> object:
        """
        Parse headers looking for their coresponding definitions in any of dlls or sources
        """

        pass
