import os
from contextlib import closing

import psycopg2
from dotenv import load_dotenv

load_dotenv()


OWNER_TABLE_CMD = """
    CREATE TABLE IF NOT EXISTS owner(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(15) NOT NULL,
        last_name VARCHAR(15) NOT NULL,
        email VARCHAR(30) NOT NULL UNIQUE
    );
"""
WAREHOUSE_TABLE_CMD = """
    CREATE TABLE IF NOT EXISTS warehouse(
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL UNIQUE,
        address VARCHAR(50) NOT NULL,
        payload INTEGER NOT NULL,
        owner_id INTEGER NOT NULL,
        FOREIGN KEY (owner_id) REFERENCES owner (id) ON DELETE CASCADE
    );
"""
VEHICLE_TABLE_CMD = """
    CREATE TABLE IF NOT EXISTS vehicle(
        id SERIAL PRIMARY KEY,
        brand VARCHAR(30) NOT NULL,
        payload SMALLINT NOT NULL,
        owner_id INTEGER NOT NULL,
        FOREIGN KEY (owner_id) REFERENCES owner (id) ON DELETE CASCADE
    );
"""
SHOP_TABLE_CMD = """
    CREATE TABLE IF NOT EXISTS shop(
        id SERIAL PRIMARY KEY,
        address VARCHAR(50) NOT NULL,
        owner_id INTEGER NOT NULL,
        FOREIGN KEY (owner_id) REFERENCES owner (id) ON DELETE CASCADE
    );
"""
PRODUCT_TABLE_CMD = """
    CREATE TABLE IF NOT EXISTS product(
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        article_number INTEGER NOT NULL UNIQUE
    );
"""
PRODUCT_SHOP_ORDER_TABLE_CMD = """
    CREATE TABLE IF NOT EXISTS product_shop_order(
        id SERIAL PRIMARY KEY,
        product_id INTEGER NOT NULL,
        shop_id INTEGER NOT NULL,
        warehouse_id INTEGER NOT NULL,
        payload SMALLINT NOT NULL,
        date_start TIMESTAMP NOT NULL,
        date_end TIMESTAMP NOT NULL,
        FOREIGN KEY (product_id) REFERENCES product (id) ON DELETE CASCADE,
        FOREIGN KEY (shop_id) REFERENCES shop (id) ON DELETE CASCADE,
        FOREIGN KEY (warehouse_id) REFERENCES warehouse (id) ON DELETE CASCADE
    );
"""
TRANSIT_TABLE_CMD = """
    CREATE TABLE IF NOT EXISTS transit(
        id SERIAL PRIMARY KEY,
        warehouse_id INTEGER NOT NULL,
        date_start TIMESTAMP NOT NULL,
        date_end TIMESTAMP NOT NULL,
        FOREIGN KEY (warehouse_id) REFERENCES warehouse (id) ON DELETE CASCADE
    );
"""
VEHICLE_TRANSIT_TABLE_CMD = """
    CREATE TABLE IF NOT EXISTS vehicle_transit(
        id SERIAL PRIMARY KEY,
        transit_id INTEGER NOT NULL,
        vehicle_id INTEGER NOT NULL,
        FOREIGN KEY (transit_id) REFERENCES transit (id) ON DELETE CASCADE,
        FOREIGN KEY (vehicle_id) REFERENCES vehicle (id) ON DELETE CASCADE
    );
"""
PRODUCT_TRANSIT_TABLE_CMD = """
    CREATE TABLE IF NOT EXISTS product_transit(
        id SERIAL PRIMARY KEY,
        transit_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        FOREIGN KEY (transit_id) REFERENCES transit (id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES product (id) ON DELETE CASCADE
    );
"""
PRODUCT_NAME_INDEX_CMD = """
    CREATE UNIQUE INDEX IF NOT EXISTS product_article_index ON product (
        name,
        article_number
    );
"""


CREATE_TABLES_CMDS = [
    OWNER_TABLE_CMD,
    WAREHOUSE_TABLE_CMD,
    VEHICLE_TABLE_CMD,
    SHOP_TABLE_CMD,
    PRODUCT_TABLE_CMD,
    PRODUCT_SHOP_ORDER_TABLE_CMD,
    TRANSIT_TABLE_CMD,
    VEHICLE_TRANSIT_TABLE_CMD,
    PRODUCT_TRANSIT_TABLE_CMD
]

CREATE_INDEXES_CMDS = [
    PRODUCT_NAME_INDEX_CMD
]


def create(db_connection, commands):
    with db_connection.cursor() as cursor:
        for cmd in commands:
            cursor.execute(cmd)
        db_connection.commit()


def main():
    with closing(psycopg2.connect(
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'))
    ) as connection:
        create(commands=CREATE_TABLES_CMDS, db_connection=connection)
        create(commands=CREATE_INDEXES_CMDS, db_connection=connection)


if __name__ == '__main__':
    main()
