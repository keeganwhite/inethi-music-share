#!/usr/bin/python3
import json
import requests


class ProductAPI:
    @staticmethod
    def create_product_entry(globalStoreModel, localStoreModel, dbModel, global_path, local_path, file_names):
        """
        Add the uploaded song to the WooCommerce store (local and global) and add
        the song to the downloads database

        :param globalStoreModel: the global store object
        :param localStoreModel: the local store object
        :param dbModel: the database object
        :param global_path: the path where the product will be stored on the global server
        :param local_path: the path where the product will be stored on the local server
        :param file_names: the list of files to be added to the stores
        :return: true if all files are added and false if they are not
        """
        # TODO add error log and check file order for db.get_upload_details
        # TODO uncomment all global calls when AWS is up again
        log_filename = "product_creation_error_log.txt"
        # Create API objects
        local_woocommerce = localStoreModel
        global_woocommerce = globalStoreModel
        db = dbModel
        for i in range(len(file_names)):
            file_name = file_names[i]

            # Read in file name and get the original name without the date time suffix
            split_file_name = file_name.split('.')
            name_with_time = split_file_name[0]  # Get the details before the file extension
            file_extension = split_file_name[1]
            temp_arr_file_name = name_with_time.split("_")
            name_without_time = temp_arr_file_name[0]
            try:
                # isolate data
                data = db.get_upload_details(db, name_without_time)
                data_as_arr = data.split("\"")
                # note the +2 to skip the character count for all of the data collection below
                username = data_as_arr[data_as_arr.index("username") + 2]
                song_name = data_as_arr[data_as_arr.index("song-name") + 2]
                selling_price = data_as_arr[data_as_arr.index("selling-price") + 2]
                band_name = data_as_arr[data_as_arr.index("band-name") + 2]
                full_description = data_as_arr[data_as_arr.index("full-description") + 2]
                category = data_as_arr[data_as_arr.index("category") + 2]
                category_as_arr = category.split(",")
                tags = data_as_arr[data_as_arr.index("tags") + 2]
                band_name_tag = local_woocommerce.generate_tag(local_woocommerce, band_name)
                band_name_tag_aws = global_woocommerce.generate_tag(local_woocommerce, band_name)
                tags_as_arr = tags.split(",")
                tags_as_arr.append(band_name)
                category_id_arr = ProductAPI.create_id_arr(
                    local_woocommerce.find_ids(local_woocommerce, category_as_arr, "category"))
                """category_id_arr_aws = ProductAPI.create_id_arr(
                    global_woocommerce.find_ids(global_woocommerce, category_as_arr, "category"))"""
                tag_id_arr = ProductAPI.create_id_arr(
                    local_woocommerce.find_ids(local_woocommerce, tags_as_arr, "tags"))
                """tag_id_arr_aws = ProductAPI.create_id_arr(
                    global_woocommerce.find_ids(global_woocommerce, tags_as_arr, "tags"))"""
                song_name = local_woocommerce.check_song_name(local_woocommerce, username, song_name)
                # song_name_aws = global_woocommerce.check_song_name(global_woocommerce, username, song_name)
                # create JSON data
                # For JSON Product Properties check http://woocommerce.github.io/woocommerce-rest-api-docs/?python#products
                data_local = {
                    "name": song_name,
                    "type": "simple",
                    "description": full_description,
                    "short_description": "Check out my profile by searching for " + username + " in the musician directory",
                    "regular_price": selling_price,
                    "virtual": True,
                    "downloadable": True,
                    "downloads": [{"name": file_name},
                                  {"file": local_path + name_with_time + "." + file_extension}],
                    "categories": category_id_arr,
                    "tags": tag_id_arr
                }

                """data_aws = {
                    "name": song_name_aws,
                    "type": "simple",
                    "description": full_description,
                    "short_description": "Check out my profile by searching for " + username + " in the musician directory",
                    "regular_price": selling_price,
                    "virtual": True,
                    "downloadable": True,
                    "downloads": [{"name": file_name},
                                  {"file": global_path + name_with_time + "." + file_extension}],
                    "categories": category_id_arr_aws,
                    "tags": tag_id_arr_aws
                }"""

                local_id = 0
                aws_id = 0
                # add to WooCommerce Store and log any errors
                try:
                    added_product = local_woocommerce.create_product(local_woocommerce, data_local)
                    local_id = added_product.get('id')
                except:
                    file = open(log_filename, "a")
                    error_msg = file_name + " could not be added local store"
                    file.write(error_msg)

                """try:
                    added_product_aws = local_woocommerce.create_product(global_woocommerce, data_aws)
                    aws_id = added_product_aws.get('id')
                except:
                    file = open(log_filename, "a")
                    error_msg = file_name + " could not be added to aws store"
                    file.write(error_msg)"""
                api_url = "http://0.0.0.0/api/initiate-download/"
                body = {
                    "songname": song_name,
                    "username": username,
                    "localID": local_id,
                    "awsID": aws_id
                }

                headers = {'Content-type': 'application/json'}
                post_request = requests.post(api_url, headers=headers, data=json.dumps(body))
                return True
            except:
                return False

    @staticmethod
    def create_id_arr(ids):
        """ Create an array of IDs in  JSON format
        :param ids: the IDs to be used
        :return: JSON formatted array
        """
        output = []
        for x in range(len(ids)):
            if x == (len(ids) - 1):
                temp = {"id": ids[x]}
                output.append(temp)
            else:
                temp = {"id": ids[x]}
                output.append(temp)
        return output
