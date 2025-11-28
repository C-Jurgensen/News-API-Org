from .Params import Param

from re import findall
from enum import Enum

__all__=["Params"]


class Params(Enum):
    country = Param("country",type=str, length=2)
    sources = Param("sources", type=str, length=2)
    category = Param("category", type=str)
    query = Param("q", length=500)
    size = Param("pageSize", type=int)
    page = Param("page", type=int, int_limit=(0,100))
    apiKey = Param("apiKey", type=str)
    sortBy = Param("sortBy", "relevancy", "popularity", "publishedAt", type=list)
    searchIn = Param("search_in", "title", "description", "content", type=list)
    excludeDomains = Param("excludeDomains", type=list)
    domains = Param("domains", type=list)
    dateFrom = Param("from")
    dateTo = Param("to")
    lang = Param("language", *findall('..',"ardeenesfrheitnlnoptrusvudzh"), type=str, length=2)

    @classmethod
    def retrieve_param(cls, item) -> Param:
        return cls[item].value
