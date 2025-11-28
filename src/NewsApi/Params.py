from .Constraints import ParamConstraint

from typing import Literal, Union

__all__ = ["Param"]

class _ParamChecker:
    """
    Default parameter option checker.
    """
    def __init__(self, options:set[Literal]):
        self.options = options

    def __call__(self, param_val):
        if not isinstance(param_val, (int, str)):
            raise TypeError('You must use a custom check for checking literals other than integers and strings.')
        if param_val not in self.options:
            raise ValueError('Value %s was not found in the declared options available.' % param_val)


class Param(ParamConstraint):
    """
    Represents a parameter that could be used and assigned to a header group.
    """
    def __init__(self, name: str, *options: Union[str,int,any], checker = None, **constraints):
        """
        Makes an instance of the Param class that can be assigned to a header group for controlling the allowable
        details that can be specified in the url.
            *If you declare options you don't need to make constraints to be checked.
        :param name: A string representing the name of the parameter.
        :param options: An iterable of options that are valid options to be passed in for this Param.
        :param checker: A custom checker is needed if your options are not of type string or integer with advanced checking
        you will need to declare a custom checker.
        :param constraints: Keyword value pairs of registered constraints referenced by name to check against the passed in value.
        """
        self.name = name
        self.__customChecker = False
        if len(options) != 0:
            if not isinstance(options, set):
                hashed_options = set()
                for option in options:
                    hashed_options.add(option)
            else:
                hashed_options:set = options
            self.checker = _ParamChecker(hashed_options) if checker is None else checker
        else:
            self.checker = checker
        super().__init__(**constraints)

    def __call__(self, value):
        """
        Performs the checking for the value passed in to the parameter at formation time.
        :param value: The value to be checked against the parameters rules.
        """
        if self.checker is not None:
            self.checker(value)
        super().check_constraints(value)
