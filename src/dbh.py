#!/usr/bin/python3
import psycopg2
from psycopg2 import extras
import config


class Dbh:

    def __init__(self):
        self._db_name = config.DB_NAME
        self._db_password = config.DB_PASSWORD
        self._db_user = config.DB_USER
        self._db_host = config.DB_HOST

    def _connect(self):
        return psycopg2.connect(dbname=self._db_name,
                                password=self._db_password,
                                user=self._db_user,
                                host=self._db_host
                                )

    def _cursor(self):
        self._connect().cursor(cursor_factory=extras.DictCursor)

    def select(self, sql, data=None) -> dict:
        conn = self._connect()
        curr = conn.cursor(cursor_factory=extras.DictCursor)
        curr.execute(sql, data)

        test: dict = {}
        identifier = 0

        for item in curr:

            result: dict = {}

            for key, value in item.items():
                result.update({key: value})

            test.update({"data" + str(identifier): result})
            identifier += 1

        curr.close()
        conn.close()

        return test
