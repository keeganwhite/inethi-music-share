#!/usr/bin/python3
import database
import store


class ProductModel:
    """
    Class containing the model needed to interact with woocommerce store and local database for use with the
    inethi-musicshare-api
    """

    def __init__(self):
        """
        Creates an object that is used to call functions that work with the WooCommerce API
        and MariaDB API
        """
        self.db = database.MusicDbModel()
        self.local_store = store.WooModel("LOCAL")
        self.global_store = store.WooModel("GLOBAL")
