import os
from contextlib import closing

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection

from create_functions import CREATE_FUNCTIONS
from create_tables import CREATE_INDEXES_CMDS, CREATE_TABLES_CMDS
from fixtures import LOAD_DATA_CMDS
from pathlib import Path

DOTENV_PATH = Path(__file__).resolve().parent.parent.joinpath('.env')

load_dotenv(dotenv_path=DOTENV_PATH)


def create(db_connection: connection, commands: list[str]) -> None:
    with db_connection.cursor() as cursor:
        for cmd in commands:
            cursor.execute(cmd)
        db_connection.commit()


def main() -> None:
    with closing(psycopg2.connect(
        database=os.getenv('DB_NAME'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'))
    ) as connection:
        create(commands=CREATE_TABLES_CMDS, db_connection=connection)
        create(commands=CREATE_INDEXES_CMDS, db_connection=connection)
        create(commands=LOAD_DATA_CMDS, db_connection=connection)
        create(commands=CREATE_FUNCTIONS, db_connection=connection)


if __name__ == '__main__':
    main()
