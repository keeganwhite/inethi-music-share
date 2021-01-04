import datetime


class MusicShareStoreAPI:
    """
        Class containing all functions needed to interact with a WooCommerce based store for use with the
        inethi-musicshare-api
    """

    @staticmethod
    def generate_tag(storeModel, tag):
        """ Used to create a tag if the tag doesn't exist

        :param storeModel: the model instance
        :param tag: the tag to generate/check if it exists
        :return: the tag ID
        """
        tag_as_arr = [tag]
        tag_data = storeModel.find_ids(storeModel, tag_as_arr, "tags")
        if len(tag_data) != 0:
            return tag_data
        else:
            data = {
                "name": tag
            }
            tag_id = storeModel.woocommerce_api.post("products/tags", data).json()
            tag_id.get("id")
            return tag_id

    @staticmethod
    def get_current_coupon_codes(storeModel):
        """ Returns all the coupon codes that are currently in the store

        :param storeModel: the model instance
        :return: a list of coupon codes (strings) that are currently in use
        """
        coupon_codes = []
        coupon_data = storeModel.woocommerce_api.get("coupons").json()
        # loop through coupon JSON objects and get codes
        for i in range(len(coupon_data)):
            coupon_codes.append(coupon_data[i].get("code"))
        return coupon_codes

    @staticmethod
    def check_if_coupon_code_exists(storeModel, code):
        """ Checks if a specified coupon code exists

        :param storeModel: the model instance
        :param code: the code
        :return: true if the coupon code exists else false
        """
        codes = storeModel.get_current_coupon_codes(storeModel)
        for x in codes:
            if x == code:
                return True
        return False

    @staticmethod
    def get_product_categories_or_tags(storeModel, type_of_data):
        """ Returns the tags or categories available in the shop

        :param type_of_data: either category or tags which is used to decide which data to get
        :param storeModel: the model instance
        :return: the tags as a dict object
        """
        if type_of_data == "tags":
            data = storeModel.woocommerce_api.get("products/tags").json()
        elif type_of_data == "category":
            data = storeModel.woocommerce_api.get("products/categories").json()
        else:
            raise Exception("Incorrect input. Second parameter should be \"tags\" or \"category\"")
        return data

    @staticmethod
    def find_ids(storeModel, items, type_of_arr):
        """ Returns the IDs of the tags or categories in the shop for specified input

        :param storeModel: the model instance
        :param items: the list of tags/categories
        :param type_of_arr: either category or tags which is used to decide which data to search through
        :return: array of tag or category IDs
        """
        if type_of_arr == "tags":
            data = storeModel.get_product_categories_or_tags(storeModel, "tags")
        elif type_of_arr == "category":
            data = storeModel.get_product_categories_or_tags(storeModel, "category")
        else:
            raise Exception("Incorrect input. Third parameter should be \"tags\" or \"category\"")
        ids = []
        # Locates the ID of the category/tag by looping through all the values returned by the store when the
        # tag/category data is queried
        for x in range(len(items)):
            for y in range(len(data)):
                if items[x] in data[y].values():  # checks if current JSON object contains the tag/category name
                    ids.append(data[y].get("id"))
                    del data[y]  # stops comparison on IDs that have already been added
                    break
        return ids

    @staticmethod
    def create_coupon(storeModel, data):
        """ Creates a coupon code

        :param storeModel: the model instance
        :param data: the JSON data to be used to create the coupon
        :return: he JSON data that was added to the store including data that is added by the store, such as IDs etc.
        """
        # print("The following coupon was added to the store:")
        data = storeModel.woocommerce_api.post("coupons", data).json()
        return data

    @staticmethod
    def create_product(storeModel, data):  # TODO add error handling and verify product is added to wp_posts
        """ Creates a product entry on the WooCommerce Store

        :param storeModel: the model instance
        :param data: the JSON data to be added to the store
        :return: the JSON data that was added to the store including data that is added by the store, such as IDs etc.
        """
        print("The following product was added:")
        product_data = storeModel.woocommerce_api.post("products", data).json()
        print(product_data)
        return product_data

    @staticmethod
    def get_product_id(storeModel, username, song_name):
        """ Get the product ID for a song a user has uploaded

        :param storeModel: the model instance
        :param username: the user name associated with the requester
        :param song_name: the song that the product ID will be added for
        :return: the ID or -1 if the song cannot be found
        """
        short_description = "<p>Check out my profile by searching for " + username + " in the musician directory</p>"
        # print(short_description)
        result = -1
        product_list = storeModel.woocommerce_api.get("products").json()
        for i in range(len(product_list)):
            temp_product = product_list[i]
            # print("Name: " + temp_product.get("name"))
            # print(temp_product.get("short_description"))
            if temp_product.get("name") == song_name and temp_product.get(
                    "short_description").strip() == short_description:
                result = temp_product.get("id")
                return result
        return result

    @staticmethod
    def check_song_name(storeModel, username, song_name):
        """ Check if a song name already exists for a particular artist and adjust it accordingly

        :param storeModel: the model instance
        :param username: the user name associated with the song that will be uploaded
        :param song_name: the song that will be added if there are no duplicates or it will be changed accordingly
        :return: the ID or -1 if the song cannot be found
        """
        short_description = "<p>Check out my profile by searching for " + username + " in the musician directory</p>"
        result = song_name
        product_list = storeModel.woocommerce_api.get("products").json()
        name_exists = True
        while name_exists:
            for i in range(len(product_list)):
                temp_product = product_list[i]
                if temp_product.get("name") == song_name and temp_product.get(
                        "short_description").strip() == short_description:
                    result = result + " (Re-Upload)"
            name_exists = False

        return result

    @staticmethod
    def get_download_count(storeModel, product_id, last_update):
        """ Iterate through the orders and add to the download counter for every order time the product has been ordered

        :param storeModel: the model instance
        :param product_id: the product that downloads will be counted for
        :param last_update: datetime object for the last update time
        :return: the number of downloads since the last update occurred
        """
        f = '%Y-%m-%d %H:%M:%S'
        downloads = 0
        # date_created_gmt
        try:
            orders = storeModel.woocommerce_api.get("orders").json()
        except:
            return 0  # no orders could be found
        for order in orders:
            if order.get("id") == product_id:
                order_time = order.get("date_created_gmt")
                order_time.replace("T", " ")  # reformat to work with datetime library
                order_time = datetime.datetime.strptime(order_time, f)
                time_delta = (order_time - last_update)
                difference = time_delta.total_seconds()
                if difference > 0:
                    downloads += 1
                else:
                    break
        return downloads
