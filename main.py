from PyQt6 import QtWidgets,uic
import db
import json
import usermodel
import quizmodel
import test
app = QtWidgets.QApplication([])#Приложение
def depricated_form():
    window = QtWidgets.QWidget()#Окно
    vl1 = QtWidgets.QVBoxLayout(window)#Вертикальное расположение виджетов
    window.setWindowTitle('Название окна')
    authbutton = QtWidgets.QPushButton('Войти') #Кнопка
    nametxt = QtWidgets.QLabel('Логин')
    namefield = QtWidgets.QTextEdit() #Поле ввода
    passtxt = QtWidgets.QLabel('Пароль')
    passfield = QtWidgets.QTextEdit() #Поле ввода
    vl1.addWidget(nametxt)
    vl1.addWidget(namefield)
    vl1.addWidget(passtxt)
    vl1.addWidget(passfield)
    vl1.addWidget(authbutton)#Добавляем на линию кнопку
    window.show()
def to_sql_date(date):
    year = date[len(date)-4:]
    month = date[3:5]
    day = date[0:2]
    sqldate = f'{year}-{month}-{day}'
    print(sqldate)
    return sqldate   
def get_user():
    file = open('user.json','r')#Открывает файл в котором хранится id пользователя
    json_user = json.load(file)#Создаём словарь из файла
    try:
        id = json_user['id']#Получаем id по ключу
        sql_user = db.get_one_by_id('users',id)#Делаем запрос к бд
        if sql_user != None:#Если данные вернулись создадим пользователя
            user = usermodel.user()
            user.createUser(sql_user)
        else:
            user = None
    except:#При появлении любой ошибки выполнения в try
        print('При получении id произошла ошибка')
        user = None #Зададим пользователя как None
    return user
def set_user(id = None):
    file = open('user.json','w')#Открываем файл
    if id != None:#Если id задан указываем этот id как значение
        user = {'id':id}
    else:#Если нет то созадём пустой словарь
        user = {}
    json.dump(user,file)#Записываем наш словарь  
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.start_up()
        self.show()
        self.setCentralWidget(self.ui)
    def start_up(self):
        self.user = get_user()
        if self.user == None:
            self.ui = LoginUi()
        else:
            self.ui = GeneralUi(self.user)
class GeneralUi(QtWidgets.QWidget):
    def __init__(self,user:usermodel.user):
        super().__init__()
        uic.loadUi('general.ui',self)
        self.findChild(QtWidgets.QLabel,'label_username').setText(user.login)#Задаём текст для надписи
        self.findChild(QtWidgets.QPushButton,'exit_button').clicked.connect(self.exit)#Задаём выход для кнопки\
        self.findChild(QtWidgets.QPushButton,'create_quiz_button').clicked.connect(self.to_create_test)
    def exit(self):
        set_user()
        mainwindow.ui = LoginUi()
        mainwindow.setCentralWidget(mainwindow.ui)
    def to_create_test(self):
        mainwindow.ui = CreateTestUi()
        mainwindow.setCentralWidget(mainwindow.ui)
class LoginUi(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('auth_form.ui',self)
        self.message_hide()
        self.findChild(QtWidgets.QPushButton,'auth_button').clicked.connect(self.auth)#На кнопку входа добавили событие при нажатии
        self.findChild(QtWidgets.QPushButton,'to_reg_button').clicked.connect(self.to_reg)
    def auth(self):
        self.message_hide()
        login = self.findChild(QtWidgets.QLineEdit,'input_login').text()
        password = self.findChild(QtWidgets.QLineEdit,'input_pass').text()
        if login != '':
            if password!='':
                query = f'''login = '{login}' and password = '{password}' '''
                result = db.get_one_by_filter('users',query)
                if result != None:
                    mainwindow.user = usermodel.user()
                    mainwindow.user.createUser(result)
                    set_user(mainwindow.user.id)
                    mainwindow.ui = GeneralUi(mainwindow.user)
                    mainwindow.setCentralWidget(mainwindow.ui)
                else:
                    self.findChild(QtWidgets.QLabel,'message_auth').setText('Аккаунт не найден')
                    self.findChild(QtWidgets.QLabel,'message_auth').show()
            else:
                self.findChild(QtWidgets.QLabel,'message_password').setText('Поле пароль не заполнено')
                self.findChild(QtWidgets.QLabel,'message_password').show()
        else:
            self.findChild(QtWidgets.QLabel,'message_login').setText('Поле логин не заполнено')
            self.findChild(QtWidgets.QLabel,'message_login').show() 
    def to_reg(self):
        mainwindow.ui = RegUi()
        mainwindow.setCentralWidget(mainwindow.ui)
    def message_hide(self):
        self.findChild(QtWidgets.QLabel,'message_login').hide()
        self.findChild(QtWidgets.QLabel,'message_password').hide()
        self.findChild(QtWidgets.QLabel,'message_auth').hide()   
class RegUi(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('reg_form.ui',self)
        self.message_hide()
        self.findChild(QtWidgets.QPushButton,'reg_button').clicked.connect(self.reg)
        self.findChild(QtWidgets.QPushButton,'back_button').clicked.connect(self.back)
    def reg(self):
        self.message_hide()
        login = self.findChild(QtWidgets.QLineEdit,'input_login').text()
        password = self.findChild(QtWidgets.QLineEdit,'input_pass').text()
        password2 = self.findChild(QtWidgets.QLineEdit,'input_repeat_pass').text()
        birthdate = to_sql_date(self.findChild(QtWidgets.QDateEdit,'input_birthday').text())
        email = self.findChild(QtWidgets.QLineEdit,'input_email').text()
        if login != '':
            if password!='':
                if password2 != '' and password2 == password:
                    query = f'''(login,password,birthdate,email)
                    VALUES('{login}','{password}','{birthdate}','{email}')'''
                    result = db.insert_one('users',query)
                    if result == None:
                        mainwindow.ui = LoginUi()
                        mainwindow.setCentralWidget(mainwindow.ui)
                    else:
                        self.findChild(QtWidgets.QLabel,'message_reg').setText('Аккаунт уже существует')
                        self.findChild(QtWidgets.QLabel,'message_reg').show()
                else:
                    self.findChild(QtWidgets.QLabel,'message_repeat_password').setText('Поле повтор пароля не заполнено')
                    self.findChild(QtWidgets.QLabel,'message_repeat_password').show()
            else:
                self.findChild(QtWidgets.QLabel,'message_password').setText('Поле пароль не заполнено')
                self.findChild(QtWidgets.QLabel,'message_password').show()
        else:
            self.findChild(QtWidgets.QLabel,'message_login').setText('Поле логин не заполненено')
            self.findChild(QtWidgets.QLabel,'message_login').show()
    def message_hide(self):
        self.findChild(QtWidgets.QLabel,'message_login').hide()
        self.findChild(QtWidgets.QLabel,'message_password').hide()
        self.findChild(QtWidgets.QLabel,'message_repeat_password').hide()
        self.findChild(QtWidgets.QLabel,'message_reg').hide()
    def back(self):
        mainwindow.ui = LoginUi()
        mainwindow.setCentralWidget(mainwindow.ui)
class CreateTestUi(QtWidgets.QWidget):
    def __init__(self,id = None):
        super().__init__()
        uic.loadUi('create_test.ui',self)
        self.scrollContent = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scrollContent)
        self.findChild(QtWidgets.QScrollArea).setWidgetResizable(True)
        self.findChild(QtWidgets.QScrollArea).setWidget(self.scrollContent)
        if id != None:
            self.test = self.get_test(id)
            self.findChild(QtWidgets.QLineEdit,'input_name').setText(self.test.name)
            self.findChild(QtWidgets.QTextEdit,'input_description').setText(self.test.description)
            for question in self.test.questions:
                pass
        else:
            self.test = quizmodel.Test(mainwindow.user)
        self.question_uis = []
        self.message_hide()
        self.findChild(QtWidgets.QScrollArea).setWidgetResizable(True)
        self.findChild(QtWidgets.QPushButton,'back_button').clicked.connect(self.back)
        self.findChild(QtWidgets.QPushButton,'create_question_button').clicked.connect(self.create_question)
        self.findChild(QtWidgets.QPushButton,'create_test_button').clicked.connect(self.create_test)
    def message_hide(self):
        self.findChild(QtWidgets.QLabel,'message_name').hide()
        self.findChild(QtWidgets.QLabel,'message_description').hide()
        self.findChild(QtWidgets.QLabel,'message_create').hide()
    def back(self):
        mainwindow.ui = GeneralUi(mainwindow.user)
        mainwindow.setCentralWidget(mainwindow.ui)
    def create_question(self):
        question = quizmodel.Question()
        self.test.add(question)
        question_ui = test.CreateQuestionUi()
        self.scroll_layout.addWidget(question_ui)
    def create_test(self):
        self.message_hide()
    def get_test(self,id):#Редактирование теста
        test = quizmodel.Test(mainwindow.user) #Создадим модель
        sql_test = db.get_one_by_id('tests',id)#Получим запись из бд в таблице tests
        test.id = id #Зададим все свойства из бд в модель
        test.name = sql_test[1]
        test.description = sql_test[2]
        for question_id in sql_test[3]:
            question = db.get_one_by_id('questions',question_id)#Получим запись из бд в таблице questions 
            newquestion = quizmodel.Question()
            newquestion.create(question)
            test.add(newquestion)
        return test



mainwindow = MainWindow()
app.exec()