#!/usr/bin/python3
import psycopg2
from psycopg2 import extras
import config


class DbIface:

    def __init__(self):
        self._db_name = config.DB_NAME
        self._db_password = config.DB_PASSWORD
        self._db_user = config.DB_USER
        self._db_host = config.DB_HOST

    def _connect(self):
        conn = 0
        try:
            conn = psycopg2.connect(dbname=self._db_name,
                                    password=self._db_password,
                                    user=self._db_user,
                                    host=self._db_host
                                    )
        except psycopg2.Error:
            print(psycopg2.Error)
        return conn

    def _cursor(self):
        self._connect().cursor(cursor_factory=extras.DictCursor)

    def _select(self, sql: str, data=None) -> dict:

        conn = self._connect()
        curr = conn.cursor(cursor_factory=extras.DictCursor)
        curr.execute(sql, data)

        result: dict = {}
        identifier: int = 0

        for item in curr:

            result: dict = {}

            for key, value in item.items():
                result.update({key: value})

            result.update({identifier: result})
            identifier += 1

        self.__close(conn, curr)
        return result

    def _exec(self, sql: str, data=None):

        conn = self._connect()
        curr = conn.cursor()
        curr.execute(sql, data)
        conn.commit()
        self.__close(conn, curr)

    @staticmethod
    def __close(conn, curr):
        curr.close()
        conn.close()
