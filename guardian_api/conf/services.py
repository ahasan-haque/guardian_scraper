from pymongo import MongoClient
from .settings import MONGO_URL


class Services:
    """
    External services are all served from here
    """

    def __init__(self):
        self.__mongo = None

    @property
    def mongo(self):
        if not self.__mongo:
            self.__mongo = MongoClient(MONGO_URL)

        return self.__mongo


services = Services()
