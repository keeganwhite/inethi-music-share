#!/bin/sh

docker-compose up -d music-wordpress
docker-compose up -d --build
