#!/usr/bin/python3
import psycopg2.extras
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
        self._connect().cursor(cursor_factory=psycopg2.extras.DictCursor)

    def execute_sql_from_file(self, filename):
        # Open and read the file as a single buffer
        fd = open(filename, 'r')
        sqlFile = fd.read()
        fd.close()

        # all SQL commands (split on ';')
        sqlCommands = sqlFile.split(';')

        conn = self._connect()
        curr = conn.cursor()

        # Execute every command from the input file
        for command in sqlCommands[:-1]:
            # This will skip and report errors
            # For example, if the tables do not yet exist, this will skip over
            # the DROP TABLE commands
            try:
                curr.execute(command)
            except psycopg2.OperationalError as msg:
                print("Command skipped: ", msg)

        conn.commit()
        conn.close()
