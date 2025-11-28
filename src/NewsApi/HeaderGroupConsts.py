from enum import Enum

from .HeaderGroups import HeaderGroup


class HeaderGroups(Enum):
    top=HeaderGroup("top-headlines", "apiKey", "country", "category", "sources", "query", "size", "page", "lang")
    everything=HeaderGroup("everything", "apiKey", "query", "searchIn", "sources", "domains", "domains", "excludeDomains",
                           "dateFrom", "dateTo", "sortBy", "size", "page", "lang")

    @classmethod
    def retr_header_group(cls, key):
        return cls[key].value
