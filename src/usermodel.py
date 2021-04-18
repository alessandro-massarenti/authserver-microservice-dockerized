from dbiface import DbIface


class UserModel(DbIface):

    def __init__(self, email: str):

        # Viene inizializzata la classe superiore
        super().__init__()

        # vengono inizializzati i campi dati
        self.__db = DbIface()
        self.__data: dict = {}
        self.__fetched: bool = False
        self.__modified: bool = False

        # La proprietà email viene settata con l'email del costruttore
        self.email = email

    def __del__(self):
        # Ci si assicura che l'ultima versione sia salvata nel database
        self.push()

    def __repr__(self):
        return self.__data

    def __fetch(self) -> None:
        self.__data = self.__db._select(sql='SELECT * FROM users.accounts WHERE email = %s;',
                                        data=(self.email,))[0]
        self.__fetched = True

    def push(self):

        # Se l'utente non esiste nel database viene inserito come nuovo
        # Se l'utente eiste nel database si cambiano i campi dati richiesti
        if self.__modified:
            self.__db._exec(
                sql='INSERT INTO users.accounts(name,surname,password,email,role) VALUES (%s,%s,%s,%s,%s)',
                data=(self.name, self.surname, self.password, self.email, "standard"))
            self.__modified = False

    @property
    def email(self) -> str:
        return self.__data['email']

    @email.setter
    def email(self, value: str):
        self.__data['email'] = value
        self.__modified = True

    @property
    def name(self) -> str:
        try:
            return self.__data['name']
        except KeyError:
            self.__fetch()

    @name.setter
    def name(self, value: str):
        self.__data['name'] = value
        self.__modified = True

    @property
    def surname(self) -> str:
        try:
            return self.__data['surname']
        except KeyError:
            self.__fetch()

    @surname.setter
    def surname(self, value: str):
        self.__data['surname'] = value
        self.__modified = True

    @property
    def password(self) -> str:
        try:
            return self.__data['password']
        except KeyError:
            self.__fetch()

    @password.setter
    def password(self, value: str):
        self.__data['password'] = value
        self.__modified = True

    @property
    def role(self) -> str:
        try:
            return self.__data['role']
        except KeyError:
            self.__fetch()

    @role.setter
    def role(self, value: str):
        self.__data['role'] = value
        self.__modified = True
