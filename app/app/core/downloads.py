import datetime
import pytz


class DownloadsAPI:
    @staticmethod
    def update_downloads(username, song_name, db, global_shop, local_shop):
        """ Update the downloads in the downloads table

        :param username: the user who owns the song
        :param song_name: the song that updates will be done for
        :param db: the local database holding the download information
        :param global_shop: the song that updates will be done for
        :param local_shop: the song that updates will be done for
        :return: the result of the process where -1 is an error, a string message to confirm that there in no need to update
        or the new total downloads
        """
        f = '%Y-%m-%d %H:%M:%S'  # the format of the MySQL date time
        # get times and find the difference between them (gmt times)
        last_update_unaware = db.get_last_update(db, username, song_name)
        # unaware of timezone
        # last_update = datetime.datetime.strptime(last_update_unaware, f)
        last_update = last_update_unaware.replace(tzinfo=pytz.UTC)

        print(last_update)
        date_time_obj_current = datetime.datetime.now(datetime.timezone.utc)
        print(date_time_obj_current)
        # date_time_obj_current = datetime.datetime.strptime(date_time_obj_current, f)
        time_delta = (date_time_obj_current - last_update)
        total_seconds_dif = time_delta.total_seconds()
        difference = total_seconds_dif / 60
        print(difference)
        #  if there hasn't been an update in over 30 minutes then update
        if difference > 30:
            id_arr = db.get_product_ids(db, username, song_name)
            id_local = id_arr[0]
            id_aws = id_arr[1]
            new_local_downloads = 0
            new_aws_downloads = 0
            if id_local != -1:
                new_local_downloads = local_shop.get_download_count(local_shop, id_local, last_update)
            if id_aws != -1:
                new_aws_downloads = global_shop.get_download_count(global_shop, id_aws, last_update)
            total_downloads = new_aws_downloads + new_local_downloads
            if total_downloads >= 0 and id_local != -1:  # if this isn't written because the DB connection fails it will
                # be updated later when the page is opened.
                new_total = db.update_downloads(db, id_local, total_downloads)
                return new_total
            else:
                return -1
        else:
            return "Has not been over 30 minutes since last update"
