import psycopg2
import pandas as pd

import json
import csv
from typing import List


def setup_db(keywords: List[str]) -> None:
    """Setups connection to heroku database and
    creates the 2 needed tables
    -----------------
    keywords (list of str): categories being searched
        for now only 3 keywords are expected
    -----------------
    secrets.json file needs to be in the root of repo with
        connection info
    """
    # Get secrets to connect to DB
    with open('./secrets.json') as f:
        secrets = f.read()
        secrets = json.loads(secrets)

    connection, cur = make_connection()

    cur.execute("""
        CREATE TABLE Keywords (
        id serial PRIMARY KEY,
        type varchar(255)
    );""")
    connection.commit()

    # TODO: helper function to automate keyword strings

    # As we know the categories we can put them in
    cur.execute(f"""
        INSERT INTO Keywords
        VALUES 
        (1, '{keywords[0]}'),
        (2, '{keywords[1]}'),
        (3, '{keywords[2]}')
        ;""")
    connection.commit()

    cur.execute("""
        CREATE TABLE Info (
        id serial PRIMARY KEY,
        title varchar(255),
        price varchar(60),
        item_url varchar(2000),
        image_url varchar(1024),
        category int,
        FOREIGN KEY (category) REFERENCES Keywords(id)
    );""")
    connection.commit()


def insert_to_db(df: pd.DataFrame) -> None:
    """Inserts dataframe into database"""
    connection, cur = make_connection()

    for row in df.itertuples(index=False):
        cur.execute(f"""
            INSERT INTO 
            Info(title, price, item_url, image_url, category)
            VALUES
            ('{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[0]}');
        """)
        connection.commit()


def export_csv(path: str) -> None:
    """Makes a join and exports data into csv"""
    connection, cur = make_connection()

    cur.execute("""
        SELECT I.title, I.price, I.item_url,
        I.image_url, K.type
        FROM Info AS I, Keywords AS K
        WHERE I.category = K.id
    ;""")

    # Fetch from DB
    data = {
        'category': [],
        'title': [],
        'price': [],
        'item_url': [],
        'img_url': [],
    }
    row = cur.fetchone()
    while row:
        data['title'].append(row[0])
        data['price'].append(row[1])
        data['item_url'].append(row[2])
        data['img_url'].append(row[3])
        data['category'].append(row[4])
        row = cur.fetchone()

    # Create a csv file
    with open(path, "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data.keys())
        writer.writerows(zip(*data.values()))


def make_connection():
    """Connects to DB
    returns connection and cur objects
    """
    # Get secrets to connect to DB
    with open('./secrets.json') as f:
        secrets = f.read()
        secrets = json.loads(secrets)

    # Connect to database
    connection = psycopg2.connect(**secrets)
    cur = connection.cursor()

    return (connection, cur)
