# Description
This is a package used to interact with the https://newsapi.org/ v2 api.

# Getting Started
Please review this to understand the features of the package.<br>
This package will require you to make an account with the above-mentioned api in order to obtain an api key.<br>
<br>
Features:
* Allows for pre-defined links with default and set parameters.
* Allows to set default values as non-mutable.
* Maps the response object allowing for search of authors and publishers.
* Has constraints set for params to prevent the sending of a request and having to handle the error or potentially 
receiving a non-favorable response.

About:
    This was originally made in order to be used with a dashboard application that will request data from the api.

## Creating a new url preset
The "URL" class in the URLs.py module is for making URL presets to be used. This is to prevent the need to handle URL parsing directly.
<br>
<br>
Constructor information:
* There's a hardcoded class attribute base url called "__baseURL" that should be changed if the url to the site and api entry changes.<br>
* Each URL will need a declared "api_key" object that will not be preset.<br>
* You must either pass in a predefined header group or make your own to pass in.<br>
* Pre declared header groups can be found in the HeaderGroupConsts.py module under the "HeaderGroups" enum. 
You can search these with the "retr_header_group" function.<br>
* "set_params" will default ot False which is no locked param values. In the future True may lock all params. All set params must have a default set.<br>
* To initiate url formation you can call the url object or call "form_url".

## Creating an API Handler
The "APIHandler" class in the __ini__.py module is directly accessible from the top of the module on import.<br>
All that needs to be set is the "api_key" parameter specified on declaration. The specified API_Key object will be used for all specified urls that you attach
to the "APIHandler" object. When you add a url to the handler object it will be added to the class instances attributes
allowing you to be able to call this directly.<br>
<br>
**Note: Say you add a url using "add_url" named "topFromRussia" you will then be able to call <Handler object>.topFromRussia()

## How param constraints work
Params
* The Params.py module contains the Param class and _ParamChecker class. The Param class should be used to create new parameters.
* Use options to declare a hashable set of options that are valid for the parameter.
* Define checker if you need value checking beyond int or str for the passed in options.
* If no options are defined no checker should be defined.
* Alternatively you can add constraints that are premate from the RegisteredConstraints.py module.
Or you may make your own constraints using the "register_your_own_constraint" decorator.

_ParamChecker
* The _ParamChecker class will be used if a custom one isn't defined.
* The default checker only checks for if the value is in the options and if it is an int or str.
On second though no idea why I had it check type? Oh well...? Pass in your own checker if you need to check for 
complex data structures or just a couple different primitives than what I passed.

## Header Groups
Make a new header group when you need to define a new header for the api that only allows for certain parameters to be used. 
<br>
<br>
HeaderGroup

* The header group takes name and parameters to make a predefined set of options for the header.
* name is the name of the header and what will be printed out for the header in the url.
* params is a list of param objects that can be used with the header.

## Calling the api with a url
Calling the api should use the ApiCaller.py module.
<br><br>
ApiCaller.py
* Use the "call_api" function passing in a url string to call the api
* Calling the api will result in an ApiResponse object.
* ApiResponse objects have metadata that contains the status and total results.
They also contain a articles object that breaks down the data into filterable sources and authors.
* Calling a url object will also invoke the "call_api" function.