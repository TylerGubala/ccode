"""
A module providing c-type header file import functionality

Upon importing this module the c header import functionality should be present.
"""

import importlib
import os
import re
import sys
import typing
from typing import Callable, List, Dict, Optional, Set

import aiofiles

class BuildEnvironment(object):
    """
    Isolates build environment functionality

    ===========
    Constructor
    ===========

    :Parameters:

        :paths: An optional agrument for the search path
    """

    def __init__(self,
                 paths: Optional[Set[str]]=None, 
                 definitions: Optional[Set[str]]=None,
                 loader: Optional[importlib.abc.Loader]=None,
                 meta_finder: Optional[importlib.abc.MetaPathFinder]=None,
                 path_entry_finder: Optional[importlib.abc.PathEntryFinder]=None):

        self.paths = paths if paths is not None else set()

        self.definitions = definitions if definitions is not None else set()

        self.loader = loader if loader is not None else CHeaderLoader(self)

        self.meta_finder = (meta_finder if meta_finder is not None else 
                            CHeaderMetaPathFinder(self))

        self.path_entry_finder = (path_entry_finder
                                  if path_entry_finder is not None else 
                                  CHeaderPathEntryFinder(self))

    def define(self, symbol:str) -> None:
        """
        Defines the symbol, throws an error if the symbol has already been defined

        :Parameters:

            :symbol: The symbol to define
        """

        if symbol in self.definitions:

            raise ValueError(f"{symbol} has already been defined")

        else:

            self.definitions.add(symbol)

    def undef(self, symbol:str) -> None:
        """
        Undefines a symbol, removing it from the definitions list

        :Parameters:

            :symbol: The symbol to undefine
        """

        if symbol not in self.definitions:

            raise ValueError(f"{symbol} has not yet been defined")

        else:

            self.definitions.discard(symbol)


class CHeaderLoader(importlib.abc.Loader):
    """
    Loads header files

    As the loader reads through the file, it finds symbols and informs its
    associated import configuration of the symbol it found. It is the
    configuration object's (and therefore the user's) responsibility to handle
    the discovered symbol, translating it some way if necessary
    """

    def __init__(self, build_environment: BuildEnvironment):

        super().__init__()

        self.build_environment = build_environment

    def exec_module(self, module: object):
        """
        Execute the header file, appending objects to the module object
        """

        filepath = module.__spec__.origin

        with open(filepath) as headerfile:

            headertext = headerfile.read()

            preprocessor_matches = re.findall(CHeaderPreProcessorDirective.REGEX,
                                              headertext)

            for preprocessor_match in preprocessor_matches:

                pass


class CHeaderMetaPathFinder(importlib.abc.MetaPathFinder):
    """
    Implimentation of the importlib's MetaPathFinder class

    Exposes the functionality to import header files, configuration is provided
    via the HImportConfiguration class
    """

    def __init__(self, build_environment: BuildEnvironment):

        self.build_environment = build_environment

    @staticmethod
    def find_spec(full_name: str,
                  path: Optional[List[str]]=None,
                  target: Optional[str]=None) -> Optional[importlib.machinery.ModuleSpec]:
        """
        Find the header (*.h) spec
        """

        path = path if path is not None else sys.path

        partial_names = full_name.split('.')

        step = 0

        for directory in path:

            for dir_path, dir_names, file_names in os.walk(directory):

                file_regex = re.compile(partial_names[step] + r'\.(h|H)')

                valid_files = [file_name for file_name in file_names if re.fullmatch(file_regex, file_name)]

                if step > len(partial_names):

                    # We could not find the module specification and or the path to the module

                    return None

                if len(valid_files) > 0:

                    file_name = valid_files[0]

                    if file_name is not None:

                        return importlib.machinery.ModuleSpec(full_name, CHeaderLoader)

                    else:

                        return None

                elif partial_names[step] in dir_names:

                    step += step

                    dir_names[:] = [dir_name for dir_name in dir_names if dir_name == partial_names[step]]

                else:

                    # We could not find the module specification and or the path to the module

                    return None

    @staticmethod
    def invalidate_caches():
        """
        Invalidate the internal cache
        """

        pass


class CHeaderPathEntryFinder(importlib.abc.PathEntryFinder):
    """
    Searches valid paths for a c header file
    """

    @staticmethod
    def find_spec(fullname: str, target: Optional[str]=None):
        """
        Search paths in the linker for c header files
        """

        pass


class CHeaderPreProcessorDirective(object):
    """
    A preprocessor directive, usually prefixed by a "#"

    In the configuration for the project there is a table of preprocessor
    directives and their python replacement equivalent
    """

    REGEX = re.compile(r'#(?P<directive_name>\w+) +(?P<directive_body>)')

    def __init__(self, name: str, pattern: re._pattern_type, func: Callable):

        pass


class CHeaderClassDefinition(object):
    """
    Represents a class defined in a header file
    """

    REGEX = re.compile(
        r'((?P<prefixes>\w*) +)*class +(?P<classname>\w+) *\{(?P<class_body>[.|\s]*)\}')

    def __init__(self, name, body):

        pass


class CHeaderFunctionDefinition(object):
    """
    Prepresents a function defined in a header file
    """

    REGEX = re.compile(r'')

    def __init__(self, name, body):

        pass
