import argparse
import sqlite3

import pandas as pd
from decouple import config

# Next steps are to create a function to query the database
# when using parameters with sql lite use the :name syntax
# ex. :name , params={"name": "value"}
# TODO 2020-08-06 create a store for database queries (aka json file)


queries = {}


def connect_to_db(db_uri):
    try:
        connection = sqlite3.connect(db_uri)
    except sqlite3.Error as e:
        print(f"{e} has occured")
    return connection


def query_db(connection, parameter):
    df = pd.read_sql(
        "Select * from Pokedex Where Type=:p_type",
        con=connection,
        params={"p_type": parameter},
        index_col="index",
    )
    return df


def main():
    db_uri = config("L_DATABASEURI")
    datafields = ["count", "min", "25%", "50%", "75%", "max"]
    prompt = argparse.ArgumentParser()
    prompt.add_argument(
        "pokemon_type",
        help="please enter the pokemon type you want to stats on:",
        default="Grass Poison",
    )
    prompt.add_argument(
        "--saveresults", help="enter the csv file name you want to save to",
    )
    args = prompt.parse_args()
    connection = connect_to_db(db_uri)
    df = query_db(connection, args.pokemon_type)
    print(f"Here are the stats for the {args.pokemon_type} pokemon.\n")
    print(df.describe().loc[datafields])
    if args.saveresults:
        df.to_csv(f"{args.saveresults}.csv", index=False)
    else:
        print("done")


if __name__ == "__main__":
    main()
