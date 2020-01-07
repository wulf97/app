class User:
    def __init__(self, login = '', password = '', name = '', surname = '', patronymic = ''):
        self.login = login
        self.password = password
        self.name = name
        self.surname = surname
        self.patronymic = patronymic

    def valid(self):
        if self.login == '':
            return False

        if self.password == '':
            return False

        if self.name == '':
            return False

        if self.surname == '':
            return False

        if self.patronymic == '':
            return False

        return True


class Student(User):
    def __init__(self, login = '', password = '', name = '', surname = '', patronymic = ''):
        User.__init__(self, login = '', password = '', name = '', surname = '', patronymic = '')
