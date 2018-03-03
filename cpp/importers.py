"""
The import facility for c++ type files
"""

import importlib
from typing import Optional

def TRANSLATE(source_text):
    """
    Use the regexes and replacement texts to create 
    """

class CppLoader(importlib.abc.Loader):
    """
    Loader for c++ type files
    """

    def create_module(self):
        """
        Return None, we'll use the default module
        """

        return None

    def exec_module(self, module: object):
        """
        Build the module from the parsed c++ data
        """

        full_path = module.__spec__.origin

        with open(full_path) as source_file:

            # We have a handle to a file

            source_text = source_file.read()

class CppMetaPathFinder(importlib.abc.MetaPathFinder):
    """
    Meta path finder for c++ type files
    """

    def find_spec(self, full_name: str, path: Optional[str] = None,
                  target: Optional[object] = None
                  ) -> Optional[importlib.machinery.ModuleSpec]:
        """
        find the c++ specification for full_name, if possible
        """

        pass
    
    def invalidate_caches(self):
        """
        Invalidate the internal cache
        """

        pass

class CppPathEntryFinder(importlib.abc.PathEntryFinder):
    """
    Path entry finder for c++ type files
    """

    def __init__(self, path_entry: str):
        
        # If the path entry is not correct for this path entry finder
        # raise an ImportError, this lets the import machenery know that
        # this PathEntryFinder is not valid for the given path, and to not
        # use it

        raise ImportError

    def find_spec(self, full_name: str, target: Optional[object] = None
        ) -> Optional[importlib.machinery.ModuleSpec]:
        """
        Find the speicification for full_name, if possible
        """

        pass
