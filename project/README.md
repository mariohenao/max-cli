# CLI for MAX-database for genres and artists

This repository provides a way to run a Command-line Interface to explore a small database.

To run the CLI is necesary to have `docker-compose>=1.29.2` and `docker>=20.10.7`.

# Project tree
The project is organized as follows:

 * [main.py](./main.py)
 * [functions.py](./functions.py)
 * [DB](./DB)
   * [data](./DB/data)
        * [artist.gz](./DB/data/artist.gz)
        * [genre.gz](./DB/data/genre.gz)
        * [genre_artist.gz](./DB/data/genre_artist.gz)
   * [connection.py](./DB/connection.py)
 * [Dockerfile](./Dockerfile)
 * [dockerfile-compose.yaml](./dockerfile-compose.yaml)
 * [README.md](./README.md)
 * [requirements.txt](./requirements.txt)

`main.py`: Runs the CLI for the use.

`functions.py`: Utilities for the CLI to display outputs.

`DB/connection.py`: Connects to the database and run SQL queries on the data.

# How to use
After cloning the repository, in the main folder run:
```
docker-compose up -d --build
```
To construct the two containers, one with the MySQL database and the other with the python environment to run the CLI. Then run the following commands: 
```
container_id=$(docker ps -qf "name=^max-service$")
docker exec -it $container_id /bin/bash
```
to execute the container and access the terminal inside the docker with the python project. (The creation of the database can take arround 1 minute)

Now, in this new terminal run:
```
python main.py
```
this runs the CLI in which the user can make the following actions:

- **List tables** -- Shows the tables in the database
- **Add new table from gzip file** -- Adds a new table from path of the file; it is recomended to add new files into `DB/data/` folder. To start it is *necesary* to add the tree starting tables in the folder `DB/data/`.
- **See table** -- Print a preview of the desired table
- **See artists starting with ___** -- Shows artists starting with the input of the user
- **See genres containing letter ___** -- Shows genres containing the input of the user
- **See the most popular genres (among artists)** -- Shows the most popular genres among the artists
- **See artists for some genre** -- Shows 10 random artists corresponding to an input genre
- **Quit** -- Quit the app
