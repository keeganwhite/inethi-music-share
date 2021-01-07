#!/usr/bin/python3
import mariadb
import json


class MusicDbModel:
    """
    Class containing the model needed to interact with a local MariaDB docker container for use with the
    inehti-musicshare-api
    """

    def __init__(self):
        """
            Creates an object that is used to call functions to interact with a mariadb container
        """
        filename = "config/database_connection_data.json.json"
        with open(filename, 'r') as file:
            self.config = json.load(file)  # loads JSON data as a dictionary
        self.host = self.config.get("host")
        self.port = self.config.get("port")
        self.user = self.config.get("user")
        self.password = self.config.get("password")
        self.database = self.config.get("database")
        # connection for MariaDB
        self.connection = mariadb.connect(**self.config)
        # create a connection cursor
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()