By Keegan White (keegan337)

An API designed to be run in tandem with a Wordpress and MongoDB docker container. The API is hosted in an Nginx and Python 3.8 hybrid docker container. This will project will eventually be incorporated into the iNethi enviroment in Ocean View South Africa. This project is an extension of an BSc Computer Science honours level thesis completed in 2020 at the University of Cape Town. The aim is to build a music sharing system for musicians to upload on local servers (data free) and allow community members to download the music. There will be a AWS hosted global version of the website where music will also be availible for download.

Build instructions:
- Setup Wordpress and MongoDB docker containers. (soon to be added to this repository)
- Wordpress must use the WooCommerce e-commerce plugin (explanation to be added)
- More to come

To do:
- Write a bash script to build the system and the realted systems from scrath for new users
- Update the docker-compose file to add the WordPress and database instance
- Add a chat bot to send artists notifications using a matrix server or something equivalent

Customisation intsructions:
- If you wish to alter the python code and use imports that aren't already used update the requirements.txt file and the prestart.sh text will make sure these are imported before your API starts up
- If you wish to expose other ports you can do so in the dockerfile using EXPOSE 'port number'
- If you wish to run the flask application in debug mode you can use the override docker compose file. This is strictly for development purposes and should not be used for production
