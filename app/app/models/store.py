#!/usr/bin/python3
from woocommerce import API
import json
import os
from dotenv import load_dotenv

class WooModel:
    """
        Class containing the model needed to interact with woocommerce store for use with the
        inethi-musicshare-api
    """

    def __init__(self, location):
        """
        Creates an object that is used to call functions that work with the WooCommerce API
        """
        load_dotenv()

        if location.upper() == "LOCAL":
            filename = os.getenv('PATH_TO_LOCAL_STORE_CONNECTION_FILE')
        elif location.upper() == "GLOBAL":
            filename = os.getenv('PATH_TO_GLOBAL_STORE_CONNECTION_FILE')
        else:
            raise ValueError("Please choose between a 'global' or 'local' configuration (not case-sensitive)")
        with open(filename, 'r') as file:
            self.config = json.load(file)  # loads JSON data as a dictionary
        self.url = self.config.get("url")
        self.pub_key = self.config.get("pub_key")
        self.secret_key = self.config.get("secret_key")
        self.woocommerce_api = API(
            url=self.url,
            consumer_key=self.pub_key,
            consumer_secret=self.secret_key,
            wp_api=True,
            version="wc/v3",
            timeout=10
        )
