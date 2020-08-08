import argparse
import configparser
import sqlite3
import pandas as pd

from pathlib import Path

DB_FILE = "database.ini"
# Next steps are to create a function to query the database
# when using parameters with sql lite use the :name syntax
# ex. :name , params={"name": "value"}
# TODO 2020-08-06 create a store for database queries (aka json file)
# TODO 2020-08-08 Add in functionality for running on windows or linux
queries = {}


def connect_to_db(db_file):
    config = configparser.ConfigParser()
    config.read(db_file)
    dbstring = Path(config["Database"]["database_string_linux"])
    try:
        connection = sqlite3.connect(dbstring)
    except error as e:
        print(f"{e} has occured")
    return connection


def query_db(connection, parameters):
    df = pd.read_sql(
        "Select * from Pokedex Where Type=:p_type",
        con=connection,
        params={"p_type": parameters},
        index_col="index",
    )
    return df


def main():
    prompt = argparse.ArgumentParser()
    prompt.add_argument(
        "pokemon_type",
        help="please enter the pokemon type you want to stats on: ",
        default="Grass Poison",
    )
    args = prompt.parse_args()
    connection = connect_to_db(DB_FILE)
    df = query_db(connection, args.pokemon_type)
    print(f"Here are the stats for the {args.pokemon_type} pokemon\n")
    print(df.describe())


if __name__ == "__main__":
    main()
