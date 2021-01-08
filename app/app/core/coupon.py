#!/usr/bin/python3
import random
import string
import os
from dotenv import load_dotenv

class CouponAPI:
    @staticmethod
    def get_random_string(length):
        """ Generate a random string (upper and lower case letters) to be used as a coupon code

        :param length: the length of the coupon code
        :return: the coupon code
        """
        # Random string with the combination of lower and upper case
        letters = string.ascii_letters
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    @staticmethod
    def create(storeModel, song_name, user, code):
        """ Gets called by the API when a coupon form is submitted

        :param storeModel: the database object
        :param code: -1 if the coupon code has not been established for one of the stores or the coupon code to be used
        to sync local and global stores
        :param song_name: song for the coupon to be made for
        :param user: the user who uploaded the song
        :return: the coupon code if it was successful or an error message
        """
        load_dotenv()
        coupon_code_length = os.getenv('COUPON_CODE_LENGTH')
        woocommerce = storeModel
        coupon_code = code
        if coupon_code == -1:
            coupon_code = CouponAPI.get_random_string(coupon_code_length)
            # print(coupon_code)
            exists = True
            while exists:
                if woocommerce.check_if_coupon_code_exists(woocommerce, coupon_code):
                    coupon_code = CouponAPI.get_random_string(coupon_code_length)
                else:
                    exists = False

        product_id = woocommerce.get_product_id(woocommerce, user, song_name)

        if product_id != -1:
            coupon_data = {
                "code": coupon_code,
                "discount_type": "percent",
                "amount": "100",
                "product_ids": [product_id],
                "usage_limit": 1
            }
            data = woocommerce.create_coupon(woocommerce, coupon_data)
            return coupon_code
        else:
            return "Cannot find the song: " + song_name + " with the user name: " + user
