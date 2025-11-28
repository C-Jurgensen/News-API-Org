__all__ = ['call_api', 'SourceId', 'SourceName', 'ApiResponse', 'Articles']

from requests import request
from typing import NamedTuple, Sequence, TypeAlias
from datetime import datetime
from logging import getLogger, INFO, WARNING

_LOGGER = getLogger(__name__)

Author = NamedTuple('Author', (('firstName', str), ('lastName', str)))
Source = NamedTuple('Source', (('id', str | None), ('name', str)))
Article = NamedTuple('Article',(('title', str),('description', str),('url', str),('urlToImage', str),('publishedAt', datetime),('content', str)))
MetaData = NamedTuple('MetaData',(('totalResults', int),))

class ResponseError(Exception):pass
class _RecordCreationError(Exception):pass
class _AuthorCreationError(_RecordCreationError):pass
class _SourceCreationError(_RecordCreationError):pass
class _ArticleCreationError(_RecordCreationError):pass


class Authors:

    """
    A class that can instantiate new authors and will keep track of the created authors.
    """

    @classmethod
    def add_author(cls, author_name:str) -> Author | None:
        """
        Checks if the author exists and creates a new one if it doesn't.
        Returns the author after creation.
        :param author_name: A string representing the author name to be created.
        :return: Author
        """
        try:
            if author_name:
                author_name = Author(*author_name.split(" "))
            return author_name
        except TypeError:
            _LOGGER.log(INFO,"Couldn't create author record: %s",_AuthorCreationError(author_name), exc_info=True)
        except Exception:
            _LOGGER.log(WARNING, "Unhandled Exception: %s", _AuthorCreationError(author_name), exc_info=True)
        return None


class SourceError(Exception):
    pass

SourceId:TypeAlias = str | None
SourceName:TypeAlias = str

class Sources:

    """
    Creates new sources and tracks the ones that were created.
    """

    @staticmethod
    def __make_source(source_raw:dict) -> Source:
        match source_raw:
            case {'id': ident, 'name': name}:
                return Source(ident, name)
            case _:
                raise SourceError('Unknown Source Format.')

    @classmethod
    def add_source(cls, source_info:dict) -> Source | None:
        """
        Checks if source exists and adds if it didn't exist.
        :param source_info: A dictionary representing the source info.
        :return: Returns an instance of __Source.
        """
        try:
            source:Source = cls.__make_source(source_info)
            return source
        except (TypeError, SourceError):
            _LOGGER.log(INFO, "Unable to create source: %s", _SourceCreationError(source_info), exc_info=True)
        except Exception:
            _LOGGER.log(WARNING, "Unhandled exception: %s", _SourceCreationError(source_info), exc_info=True)
        return None


class Articles(Authors, Sources):

    """
    Keeps an active record of all articles in the response object.
    """

    def __init__(self, articles:Sequence):
        self.articles:list[tuple[Source, Author, Article]] = list()
        self.articles.extend(self.__make_article_record(article_raw) for article_raw in articles if not None)

    def __make_article_record(self, article_raw:dict) -> tuple[Source|None ,Author|None, Article] | None:
        """
        Takes the raw article data from the response articles section.
        :param article_raw: Raw article dictionary object.
        :return: Returns either an Article object, nothing, or throws an ArticleRecordError.
        """
        match article_raw:
            case {'source':{**source_raw}, 'author':author_raw, **article_data}:
                try:
                    source:Source | None; author:Author | None; article:Article
                    record = (self.add_source(source_raw), self.add_author(author_raw), Article(**article_data))
                    return record
                except TypeError:
                    _LOGGER.log(INFO, "Ran into an error creating article object: %s", _ArticleCreationError(article_data), exc_info=True)
                except Exception:
                    _LOGGER.log(WARNING, "Unhandled exception: %s", _RecordCreationError(article_raw), exc_info=True)
            case _:
                _LOGGER.log(INFO, "Unpatterned article: %s",_ArticleCreationError(article_raw), exc_info=True)
        return None


class ApiResponse:

    """
    Keeps articles if any and metadata from response.
    """

    def __init__(self, response:dict):
        """
        Takes the response parsed into a dictionary from the response.
        :param response: The object returned from the parsed api response.
        """
        self.metadata:MetaData; self.articles:Articles
        self.metadata, self.articles = self.__match_response(response)

    @staticmethod
    def __match_response(response_obj:dict) -> tuple[MetaData, Articles]:
        """
        Takes the response object and returns a tuple of the metadata and articles or throws an error.
        :param response_obj: A dictionary parsed from the json response received from the api.
        :return: A metadata object and articles class instance populated with articles from the response.
        """
        match response_obj:
            case {'status':'ok', 'totalResults':total_results, 'articles':[*articles]}:
                return MetaData(total_results), Articles(articles)
            case {'status':'error', 'code':code, 'message':message}:
                raise ResponseError('Error Code: %s\nMessage: %s' %(code, message))
            case _:
                raise ResponseError('Not yet patterned response: %s'%response_obj)


def call_api(url:str) -> ApiResponse:
    return ApiResponse(request('GET', url).json())
