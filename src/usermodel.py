from dbiface import DbIface


class UserModel(DbIface):

    def __init__(self, email: str):
        super().__init__()
        self.__db = DbIface()
        self.__data = {'email': email}
        self.__modified: bool = False
        self.__fetched: bool = False

    def __del__(self):
        if self.__modified:
            # if __data has been modified it updates it on db
            pass

    def __repr__(self):
        return self.__data

    def __fetch(self) -> None:
        self.__data = self.__db._select(sql='SELECT * FROM users.accounts WHERE email = %s;',
                                        data=(self.__data['email'],))[0]
        print(self.__data)
        self.__fetched = True

    def push(self):
        if not self.__fetched:
            self.__data = self.__db._insert(
                sql='INSERT INTO users.accounts(name,surname,password,email,role) VALUES (%s,%s,%s,%s,%s)',
                data=(self.name, self.surname, self.password, self.email, "standard"))

    @property
    def email(self) -> str:
        if not self.__fetched:
            self.__fetch()
        return self.__data['email']

    @email.setter
    def email(self, value: str):
        self.__data['email'] = value
        self.__fetched = False

    @property
    def name(self) -> str:
        if not self.__fetched:
            self.__fetch()
        return self.__data['name']

    @name.setter
    def name(self, value: str):
        self.__data['name'] = value
        self.__fetched = False

    @property
    def surname(self) -> str:
        if not self.__fetched:
            self.__fetch()
        return self.__data['surname']

    @surname.setter
    def surname(self, value: str):
        self.__data['surname'] = value
        self.__fetched = False

    @property
    def password(self) -> str:
        if not self.__fetched:
            self.__fetch()
        return self.__data['password']

    @password.setter
    def password(self, value: str):
        self.__data['password'] = value
        self.__fetched = False

    @property
    def role(self) -> str:
        if not self.__fetched:
            self.__fetch()
        return self.__data['role']

    @role.setter
    def role(self, value: str):
        self.__data['role'] = value
        self.__fetched = False
