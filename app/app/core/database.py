#!/usr/bin/python3
import mariadb
import datetime


class MusicShareDbAPI:
    """
    Class containing all functions needed to interact with a local MariaDB docker container for use with the
    inethi-musicshare-api
    """

    @staticmethod
    def add_user(dbModel, username, hashed_password):
        """ Adds user to the API database

        :param dbModel: the instance of the model
        :param username: the user to be added
        :param hashed_password: the hash of their password
        :return: true if the user wsa added and false if it was not
        """
        try:
            dbModel.cursor.execute("INSERT INTO `users`(`user_name`, `password`) VALUES (?, ?)",
                                   (username, hashed_password))
            dbModel.connection.commit()  # commit changes
        except mariadb.Error as e:
            print(f"Error: {e}")
            return False
        return True

    @staticmethod
    def check_for_user(dbModel, username):
        """ Check if a user is already inb the database

        :param dbModel: the instance of the model
        :param username: the user to check
        :return: true if the user exists or false if they do not/there's an error
        """
        sql_command = "SELECT `user_name` FROM `users` WHERE `user_name` = '" + username + "'"
        try:
            dbModel.cursor.execute(sql_command)
        except mariadb.Error as e:
            print(f"Error: {e}")
            return False
        user = []
        for (user_name) in dbModel.cursor:
            if user_name is not None:
                user.append(user_name)
        if len(user) == 0:
            return False
        return True

    @staticmethod
    def get_user_id(dbModel, username):
        """ Get the user's ID using their username

        :param dbModel: the instance of the model
        :param username: the user to get the ID for
        :return: -1 if there's am error or the user does not exist or the user's ID
        """
        sql_command = "SELECT `id` FROM `users` WHERE `user_name` = '" + username + "'"
        try:
            dbModel.cursor.execute(sql_command)
        except mariadb.Error as e:
            print(f"Error: {e}")
            return -1
        id_arr = []
        for (id) in dbModel.cursor:
            if id is not None:
                id_arr.append(id)
        if len(id_arr) == 0:
            return -1
        else:
            id = id_arr[0]
            result = id[0]
            return result

    @staticmethod
    def get_user_name_with_id(dbModel, id):
        """ Get the user's username using their ID

        :param dbModel: the instance of the model
        :param id: the ID of the user
        :return: -1 if there's am error or the user does not exist or the user's username
        """
        sql_command = "SELECT `user_name` FROM `users` WHERE `id` = " + id
        try:
            dbModel.cursor.execute(sql_command)
        except mariadb.Error as e:
            print(f"Error: {e}")
            return -1
        user = []
        for (user_name) in dbModel.cursor:
            if user_name is not None:
                user.append(user_name)
        if len(user) == 0:
            return -1
        else:
            userName = user[0]
            result = userName[0]
        return result

    @staticmethod
    def get_user_password(dbModel, username):
        """ Get the user's hashed password

        :param dbModel: the instance of the model
        :param username: the user's username
        :return: the hashed password or -1 if it cannot be retrieved or the user is not registered
        """
        sql_command = "SELECT `password` FROM `users` WHERE `user_name` = '" + username + "'"
        try:
            dbModel.cursor.execute(sql_command)
        except mariadb.Error as e:
            print(f"Error: {e}")
            return -1
        passW = []
        for (password) in dbModel.cursor:
            if password is not None:
                passW.append(password)
        if len(passW) == 0:
            return -1
        else:
            pass_arr = passW[0]
            result = pass_arr[0]
            return result

    @staticmethod
    def get_last_update(dbModel, username, song_name):
        """ Gets the time the last download count update occurred

        :param dbModel: the instance of the model
        :param username: the name of the user who uploaded thee song
        :param song_name: the song that the downloads belong to
        :return: the last update time or -1 if it cannot be retrieved
        """
        sql_command = "SELECT `last_updated` FROM `downloads` WHERE `song_name` = '" + song_name + "' AND `username` = '" + username + "'"
        try:
            dbModel.cursor.execute(sql_command)
        except mariadb.Error as e:
            print(f"Error: {e}")
        dateArr = []
        for (last_updated) in dbModel.cursor:
            if last_updated is not None:
                dateArr.append(last_updated)
        if len(dateArr) == 0:
            return -1
        else:
            date = dateArr[0]
            result = date[0]
        return result

    @staticmethod
    def get_product_ids(dbModel, username, song_name):
        """ Get the global and local product IDs from the store

        :param dbModel: the instance of the model
        :param username: the user who uploaded the song
        :param song_name: the name of the song that is being queried
        :return: ann array with the IDs, with -1 in place of an ID that could not be retrieved
        """
        # has to be split into two queries because of how the cursor works
        sql_command = "SELECT `local_product_id` FROM `downloads` WHERE `song_name` = '" + song_name + "' AND `username` = '" + username + "'"
        try:
            dbModel.cursor.execute(sql_command)
        except mariadb.Error as e:
            print(f"Error: {e}")
        idArr = []
        local_id = []
        for (local_product_id) in dbModel.cursor:
            if local_product_id is not None:
                local_id.append(local_product_id)
        if len(local_id) == 0:
            idArr.append(-1)
        else:
            loc_id = local_id[0]
            temp = loc_id[0]
            idArr.append(temp)
        sql_command = "SELECT `global_product_id` FROM `downloads` WHERE `song_name` = '" + song_name + "' AND `username` = '" + username + "'"
        try:
            dbModel.cursor.execute(sql_command)
        except mariadb.Error as e:
            print(f"Error: {e}")
        aws_id = []
        for (local_product_id) in dbModel.cursor:
            if local_product_id is not None:
                aws_id.append(local_product_id)
        if len(aws_id) == 0:
            idArr.append(-1)
        else:
            aws = aws_id[0]
            temp = aws[0]
            idArr.append(temp)
        return idArr

    @staticmethod
    def update_downloads(dbModel, local_id, new_downloads):
        """ Update download count in the database

        :param dbModel: instance of the class
        :param local_id: the local ID of the song
        :param new_downloads: the new downloads to be added to the download count
        :return: the total downloads or -1 if it fails
        """
        local_id = str(local_id)
        sql_command = "SELECT `amnt_downloads` FROM `downloads` WHERE `local_product_id` = '" + local_id + "'"
        try:
            dbModel.cursor.execute(sql_command)
        except mariadb.Error as e:
            print(f"Error: {e}")
            return -1
        downloads = []
        for (amnt_downloads) in dbModel.cursor:
            if amnt_downloads is not None:
                downloads.append(amnt_downloads)
        if len(downloads) == 0:
            return -1
        else:
            dwn = downloads[0]
            temp = dwn[0]
            total_downloads_as_int = temp + new_downloads
            total_downloads = str(total_downloads_as_int)
        current_time_as_str = str(datetime.datetime.now(datetime.timezone.utc))
        current_time_as_str_arr = current_time_as_str.split(".")
        current_time_as_str = current_time_as_str_arr[0]
        print(current_time_as_str)
        # , `last_updated` = '" + current_time_as_str + "'
        sql_command = "UPDATE `downloads` SET `amnt_downloads` = '" + total_downloads + "', `last_updated` = '" + current_time_as_str + "' WHERE `local_product_id` = '" + local_id + "'"
        try:
            dbModel.cursor.execute(sql_command)
            dbModel.connection.commit()
            print("done update downloads amount")
        except mariadb.Error as e:
            print(f"Error: {e}")
            return -1

        return total_downloads_as_int

    @staticmethod
    def initiate_download(dbModel, song_name, username, local_id, global_id):
        """ When a product is created this is called to create an entry in the downloads table and set he downloads to 0

        :param dbModel: the instance of the model
        :param song_name: the song that has been create
        :param username: the user who uploaded the song
        :param local_id: the product ID from the local store
        :param global_id: the product ID from the AWS hosted store
        :return: true if it is initiated or false if it isn't
        """
        try:
            dbModel.cursor.execute(
                "INSERT INTO `downloads`(`song_name`, `username`, `local_product_id`, `global_product_id`, `amnt_downloads`) VALUES (?, ?, ?, ?, ?)",
                (song_name, username, local_id, global_id, 0))
            dbModel.connection.commit()
        except mariadb.Error as e:
            print(f"Error: {e}")
            return False
        return True

    @staticmethod
    def get_upload_details(dbModel, file_name):
        """ Get contact form 7 value for the upload, which contains all the details needed to create the song in the shop

        :param file_name:
        :param dbModel:
        :param file_name: the file that has been added to the wordpress user-upload folder that triggers
        this script to run
        :return: the data needed to creat the WooCommerce product or -1 if the db read fails
        """
        upload_data = []
        like_formatted_name = "%uploads%" + file_name + "%"  # include uploads to ignore any other forms submitted
        sql_command = "SELECT form_value FROM `wp_db7_forms` WHERE form_value like '" + like_formatted_name + "' ORDER BY `form_date` DESC LIMIT 1 "
        try:
            dbModel.cursor.execute(sql_command)
        except mariadb.Error as e:
            print(f"Error: {e}")
            return -1
        for (form_value) in dbModel.cursor:
            upload_data.append(form_value)
        upload_data_tuple = upload_data[0]
        result = upload_data_tuple[0]
        return result
