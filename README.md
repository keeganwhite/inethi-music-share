**Please note this project is no longer active. Please see updated projects on the [iNethi GitHub profile](https://github.com/iNethi).**

# Contributors
Keegan White (keegan337)

# Description
An API designed to be run in tandem with a Wordpress and MongoDB docker container. The API is hosted in an Nginx and Python 3.8 hybrid docker container. This will project will eventually be incorporated into the iNethi environment in Ocean View South Africa. This project is an extension of an BSc Computer Science honours level thesis completed in 2020 at the University of Cape Town. The aim is to build a music sharing system for musicians to upload on local servers (data free) and allow community members to download the music. There will be a AWS hosted global version of the website where music will also be available for download.

# Usage

## Build instructions:
- Setup Wordpress and MongoDB docker containers. (my mounted files cannot be added to this repo as it contains public and private keys as well as password information). *YOUR DATA* should be added to the wp-content file and database-dumps file
- Wordpress must use the WooCommerce e-commerce plugin as well as... (to be added)

## Customisation instructions:
- If you wish to alter the python code and use imports that aren't already used update the requirements.txt file and the prestart.sh text will make sure these are imported before your API starts up
- If you wish to run the flask application in debug mode you can use the override docker compose file found in the debug-scripts folder. This is strictly for development purposes and should not be used for production.

## Migration and setup
To migrate Wordpress instances between different servers:
1. Compress wp-content folder from the version of the website you wish migrate. Export the corresponding database using adminer.
2. Startup new mariadb and adminer using the local_build_database_and_folders.sh file on the new server:
3. Import database at adminer using the database export created in step 1. (make sure the URL is updated to the current URL being used in the database. This can be changed easily pre-import by editing the text file.)
4. Start up the wordpress and api docker containers with the wp-content file in the correct place using the local_build_wordpress.sh
5. Go to the sites URL and everything should load correctly.
6. Setup cronjob to run product_creation.sh

# To do:
- Add a chat bot to send artists notifications using telegram
- Add wordpress plugin list so people can recreate the site
