import os
from contextlib import closing

import psycopg2
from dotenv import load_dotenv

from create_tables import CREATE_TABLES_CMDS, CREATE_INDEXES_CMDS
from fixtures import LOAD_DATA_CMDS

load_dotenv()


def create(db_connection, commands: list[str]) -> None:
    with db_connection.cursor() as cursor:
        for cmd in commands:
            cursor.execute(cmd)
        db_connection.commit()


def main() -> None:
    with closing(psycopg2.connect(
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'))
    ) as connection:
        create(commands=CREATE_TABLES_CMDS, db_connection=connection)
        create(commands=CREATE_INDEXES_CMDS, db_connection=connection)
        create(commands=LOAD_DATA_CMDS, db_connection=connection)


if __name__ == '__main__':
    main()
