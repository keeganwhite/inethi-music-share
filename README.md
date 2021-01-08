By Keegan White (keegan337)

An API designed to be run in tandem with a Wordpress and MongoDB docker container. The API is hosted in an Nginx and Python 3.8 hybrid docker container. This will project will eventually be incorporated into the iNethi environment in Ocean View South Africa. This project is an extension of an BSc Computer Science honours level thesis completed in 2020 at the University of Cape Town. The aim is to build a music sharing system for musicians to upload on local servers (data free) and allow community members to download the music. There will be a AWS hosted global version of the website where music will also be available for download.

Build instructions:
- Setup Wordpress and MongoDB docker containers. (soon to be added to this repository)
- Wordpress must use the WooCommerce e-commerce plugin (explanation to be added)
- More to come

Customisation instructions:
- If you wish to alter the python code and use imports that aren't already used update the requirements.txt file and the prestart.sh text will make sure these are imported before your API starts up
- If you wish to expose other ports you can do so in the dockerfile using EXPOSE 'port number'
- If you wish to run the flask application in debug mode you can use the override docker compose file. This is strictly for development purposes and should not be used for production

Migration and setup (needs to be updated and bash script will do this for you)
To migrate Wordpress instances between different servers:
1. Compress wp-content folder from the version of the website you wish migrate. Export the corresponding database using adminer (at port 8080)
2. Startup new mariadb and adminer using the docker-compose.yml file on the new server:
  docker-compose up -d inethi-musicshare-mariadb
  docker-compose up -d ineth-musicshare-adminer
3. Import database at 8080 using the database export created in step 1. (make sure the URL is updated to the current URL being used in the database. This can be changed easily pre-import by editing the text file.)
4. Start up wordpress with the wp-content file in the correct place using the docker-compose.yml file on the new server:
  docker-compose up -d inethi-musicshare
5. Go to the URL and everything should load correctly.
6. Run:
   docker exec -t -i inethi-musicshare-mariadb bash
    apt-get update
    apt-get install vim
    vi /etc/mysql/my.cnf
    THEN UPDATE: "secure-file-priv = NULL" to "secure-file-priv = /var/lib/mysql". Save that exit the container and then run:
    docker restart inethi-musicshare-mariadb
7. Start the API using its docker file or the 'docker-compose up -d --build' command. Can update database at any time.
8. Setup cronjob to run product_creation.sh

To do:
- Write a bash script to build the system and the related systems from scratch for new users
- Update the docker-compose file to add the WordPress and database instance
- Add a chat bot to send artists notifications using a matrix server or something equivalent
