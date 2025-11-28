from .ApiCaller import ApiResponse
from .ApiKey import ApiKey
from .HeaderGroups import HeaderGroup
from .HeaderGroupConsts import HeaderGroups
from .ApiCaller import call_api

from typing import Union

__all__=["URL"]

EVERYTHING = HeaderGroups.everything.value
TOP_ARTICLES = HeaderGroups.top.value

class URL:

    __baseURL = 'https://newsapi.org/v2/'

    def __init__(self, api_key:Union['ApiKey',str] = None, /, header: HeaderGroup = HeaderGroups.top.value, set_params:tuple | bool = False, **param_defaults):
        """
        Declares a url object for parameters to be entered into.
        :param header: The headerGroup to use.
        :param set_params: All set params must have a set default value.
        :param editable_params: A keyword dictionary of parameters to be searched.
        """
        if isinstance(api_key, str):
            api_key = ApiKey(api_key)
        if api_key is not None and not isinstance(api_key, ApiKey):
            raise TypeError('Api key is not of the proper type.')
        self.__apiKey = api_key
        self.__header = header
        self.__setParams:set|bool = set(set_params) if isinstance(set_params, tuple) else set_params
        self.__paramDefaults:dict|None = param_defaults
        self.__paramDefaults['apiKey'] = self.__apiKey

    @property
    def param_defaults(self):
        """
        Returns a shallow copy of the default parameters.
        """
        return self.__paramDefaults.copy()

    @property
    def set_params(self):
        return self.__setParams

    def set_api_key(self, key):
        """
        Sets a new api key.
        :param key: An instance of the ApiKey class.
        """
        if not isinstance(key, ApiKey):
            raise TypeError('"key" must be of type %s' % ApiKey)
        self.__apiKey = key

    def update_defaults(self, **params):
        """
        Changes the default parameter values.
        """
        self.__header.check_params(**params) #Check if the new values are acceptable for the header and param constraints.
        self.__paramDefaults.update(params)

    def form_url(self, **params):
        """
        Returns a formatted url to be sent as an HTTP request.
        :param params: Parameter values to be passed into at format time. These will overwrite non set defaults.
        These values still need to be defined within the header group assigned to the URL.
        """
        if self.__apiKey is None:
            raise ValueError('You must define an API key.')
        self.__header.check_params(**params)
        url_structure = [self.__header.name]
        if type(self.__setParams) == set and len(self.__setParams.intersection(set(params.keys()))) != 0:
            # Checks for any parameters that were set as non-editable.
            raise KeyError\
                (
                    'The following parameters were set as non-editable: %s' \
                    % self.__setParams.intersection(set(params.keys()))
                )
        for param in set(self.__paramDefaults.keys()).difference(set(params.keys())):
            # Updates the parameters with default params that weren't overwritten.
            params[param] = self.__paramDefaults[param]
        return self.__baseURL+'/'.join(url_structure)+'?'+'&'.join(['%s=%s' % (param, value) for param, value in params.items()])

    def __str__(self):
        return self.form_url()

    def __call__(self) -> ApiResponse:
        """
        Calls the api with the current url and returns an api response object.
        """
        return call_api(self.form_url())
