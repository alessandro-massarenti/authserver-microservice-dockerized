class User:

    def __init__(self, dbdata: list):
        self._data = dbdata

    @property
    def _name(self) -> str:
        return self._data[0]

    @property
    def _surname(self) -> str:
        return self._data[1]

    @property
    def _password(self) -> str:
        return self._data[2]

    @property
    def _email(self) -> str:
        return self._data[3]

    @property
    def _role(self):
        return self._data[4]