from psycopg2 import extras
import config
from dbiface import DbIface


class UserModel(DbIface):

    def __init__(self, email: str):
        super().__init__()
        self.__db = DbIface()
        self.__data = {'email': email}
        self.__modified: bool = False

    def __del__(self):
        if self.__modified:
            # if __data has been modified it updates it on db
            pass

    def __repr__(self):
        return self.__data

    def __fetch(self) -> None:
        self.__data = self.__db._select(sql='SELECT * FROM users.accounts')

    @property
    def email(self):
        return self.__data['email']

    @property
    def name(self) -> str:
        return self.__data['name']

    @property
    def surname(self) -> str:
        return self.__data['surname']

    @property
    def password(self):
        return self.__data['password']

    @property
    def role(self):
        return self.__data['role']
