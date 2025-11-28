from .RegisteredConstraints import check_constraints

__all__=["ParamConstraint"]


class ParamConstraint:

    def __init__(self, **kwargs):
        """
        Makes a group of constraints.
        :param kwargs: A dictionary of keyword value pairs that create instances of registered constraints to be implemented.
        """
        self.__constraints = list()
        for key, value in kwargs.items():
            constraint_handler = check_constraints(key)
            if constraint_handler is None:
                raise KeyError('No handler found for constraint %s' % key)
            self.__constraints.append(constraint_handler(value))

    def check_constraints(self, value:any):
        """
        Checks if the value passed in meets all the constraints for this parameter.
        """
        for constraint in self.__constraints:
            constraint(value)
