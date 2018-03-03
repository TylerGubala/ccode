"""
Classes and methods for c++ function declaration handling
"""

from ..transpile import abstract

class CppFunction(abstract.AbstractSymbol):
    """
    A c++ function definition
    """
    
    SEARCH_PATTERN = (r'(?P<function_decl_pre_whitespace>[ \t]*)function)'
                      r'(?P<function_declaration_post_whitesapce>[ \t]+)'
                      r'(?P<function_name>\w+)'
                      r'(?P<function_name_post_whitespace>[ \t]*)\('
                      r'(?P<function_parameters>'
                      r'(?P<function_parameter>('
                      r'(?P<function_parameter_type>))))')

    @property
    def REPLACE_PATTERN(self):
        """
        The reaplcement pattern to use when matching the text
        """

        return ("")