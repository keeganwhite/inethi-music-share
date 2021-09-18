#!/bin/sh

sudo mkdir /mnt/data/inethi-music-share/
sudo mkdir /mnt/data/inethi-music-share/wordpress
sudo mkdir /mnt/data/inethi-music-share/wordpress/wp-content
sudo mkdir /mnt/data/inethi-music-share/wordpress/wp-content/
sudo cp -r ./data/wp-content/* /mnt/data/inethi-music-share/wordpress/wp-content/
sudo mkdir /mnt/data/inethi-music-share/mariadb
sudo chmod -R 775 /mnt/data/inethi-music-share/
docker-compose up -d music-mariadb
docker-compose up -d music-adminer
