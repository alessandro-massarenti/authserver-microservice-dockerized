from old.dbh import Dbh
from psycopg2.extras import RealDictCursor


class Users(Dbh):
    class User:

        def __init__(self, dbdata: list):
            self._data = dbdata
            self._name = dbdata[0]
            self._surname = dbdata[1]
            self._password = dbdata[2]
            self._email = dbdata[3]
            self._role = dbdata[4]

        @property
        def name(self) -> str:
            return self._data[0]

        @property
        def surname(self) -> str:
            return self._data[1]

        @property
        def password(self) -> str:
            return self._data[2]

        @property
        def email(self) -> str:
            return self._data[3]

        def json(self):
            return self.name


    def __init__(self):
        super().__init__()
        # try:
        #    self.get_users()
        # except psycopg2.ProgrammingError:
        #    self.generate_db_structure()

    def get_users(self):
        sql = 'SELECT * FROM users.accounts'
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(sql)

        result = cur.fetchall()

        cur.close()
        conn.close()

        # print(result)
        return result

    def get_user(self, email) -> User:
        sql = 'SELECT * FROM users.accounts WHERE email = %s'
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(sql, (email,))

        row = cur.fetchone()
        cur.close()
        conn.close()

        result: User = User(row)

        return result

    def create_user(self, name, surname, password, email, role="standard"):
        sql = 'INSERT INTO users.accounts (name, surname, password, email, role)' \
              'VALUES (%s, %s,%s,%s,%s);'
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(sql, (name, surname, password, email, role,))

        cur.commit()
        conn.close()

    def get_password_hash(self, email):
        sql = 'SELECT password FROM users.accounts WHERE email = %s'
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(sql, (email,))

        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def get_permission(self, name: str):
        sql = """SELECT DISTINCT permissions.rule from users.permissions
                    JOIN users.roles_permissions rp on permissions.rule = rp.permit
                    JOIN users.roles r on rp.role = r.name
                    JOIN users.accounts a on r.name = a.role
                    WHERE a.name LIKE %s;"""
        conn = self._connect()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql, (name,))
        result = cur.fetchall()
        cur.close()
        conn.close()

        return result

    def generate_db_structure(self):
        self.execute_sql_from_file('../../data_structure.sql')

