class user():
    def __init__(self):
        self.id = ''
        self.login = ''
        self.birthdate = ''
        self.email = ''
    #Создание объекта пользователя
    def createUser(self,data):
        self.id = data[0]
        self.login = data[1]
        self.email = data[2]
        self.birthdate = data[5]
