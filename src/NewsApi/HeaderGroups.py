from .Params import Param
from .ParamConstraintsConsts import Params

__all__=["HeaderGroup"]

class HeaderGroup:

    def __init__(self, name:str, *params:str):
        """
        Instances header group creating a group of parameters to be used for a specific header.
        :param name: The name to be printed out for the header group in url formation.
        :param params: Parameter objects referenced by name from the Params class from the ParamConstraintsConsts
        module to be used in the header group.
        """
        self.__name:str = name
        self.__params:dict[str,Param] = {} #A dictionary of the param name and parameter.
        self.add_params(*params) #Adding initial passed in parameters.

    @property
    def name(self):
        """
        Returns the name of the header group.
        """
        return self.__name

    def add_params(self, *params:str):
        """
        Adds in the new parameter value sto the params dictionary.
        :param params: An iterable of initialized parameters to be assigned to the header group.
        """
        for param in params:
            param_obj:Param = Params.retrieve_param(param)
            if isinstance(param, Param):
                raise TypeError('Param needs to be of type param. Got: %s' % type(param))
            self.__params[param] = param_obj

    def check_params(self, **params):
        """
        Checks if the passed in parameters are valid for the header.
        :param params: A keyword value pair of params passed in to be checked.
        """
        for param, value in params.items():
            if parameter := self.__params.get(param):
                parameter(value)
            else:
                raise KeyError('Parameter "%s" is not in header group "%s".' %(param, self.name))

    def __str__(self):
        return self.__name

    def __repr__(self):
        return self.__name