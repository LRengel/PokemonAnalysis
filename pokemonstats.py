import argparse
import sqlalchemy
import pandas as pd
from decouple import config

# Next steps are to create a function to query the database
# when using parameters with sql lite use the :name syntax
# ex. :name , params={"name": "value"}
# TODO 2020-08-06 create a store for database queries (aka json file)
# TODO 2020-09-07 deal with connecting to different dbs

# This removes repeated name mega name with just name mega
# df.Name.replace({r'^\w+Mega\s': "Mega "}, regex=True, inplace=True)


def connect_db_alchemy(db_uri):
    connection = None
    try:
        connection = sqlalchemy.create_engine(db_uri)
        return connection
    except sqlalchemy.exc.IntegrityError as e:
        print(f"{e} occured")
    return connection


def query_db(connection, parameter1, parameter2):
    df = pd.read_sql(
        "Select * from Pokedex Where Type_1=:p_type and Type_2=:sec_type",
        con=connection,
        params={"p_type": parameter1, "sec_type": parameter2},
        index_col="id",
    )
    return df


def main():
    db_uri = config("L_DB_STRING")
    # datafields = ["count", "min", "25%", "50%", "75%", "max"]
    prompt = argparse.ArgumentParser()
    prompt.add_argument(
        "pokemon_type1", help="please enter the pokemon type1 you want to stats on:"
    )
    prompt.add_argument(
        "pokemon_type2", help="please enter the pokemon type2 you want to stats on:"
    )
    prompt.add_argument(
        "--saveresults",
        action="store_true",
        help="enter the csv file name you want to save to",
    )
    args = prompt.parse_args()
    connection = connect_db_alchemy(db_uri)
    df = query_db(connection, args.pokemon_type1, args.pokemon_type2)
    if args.pokemon_type2 == " ":
        print(f"\nHere are the stats for the {args.pokemon_type1} type pokemon.\n")
    else:
        print(
            f"\nHere are the stats for the {args.pokemon_type1} and {args.pokemon_type2} type pokemon.\n"
        )
    print(f"{df.describe()}\n")
    if args.saveresults:
        df.to_csv(f"{args.saveresults}.csv", index=False)
    else:
        print("Query Completed")


if __name__ == "__main__":
    main()
