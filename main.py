from PyQt6 import QtWidgets,uic
import db
import json
import usermodel
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
def auth():
    global window
    login = window.input_login.text()
    password = window.input_pass.text()
    if login != '':
        if password!='':
            query = f'''login = '{login}' and password = '{password}' '''
            result = db.get_one_by_filter('users',query)
            if len(result) > 0:
                global user
                user = usermodel.user()
                user.createUser(result)
                set_user(user.id)
                window = GeneralUi()
        else:
            print('Пароль не заполнен')
    else:
        print('Поле логин не заполнено')
def reg():
    login = window.input_login.text()
    password = window.input_pass.text()
    password2 = window.input_repeat_pass.text()
    birthdate = to_sql_date(window.input_birthday.text())
    email = window.input_email.text()
    if login != '':
        if password!='':
            if password2 != '' and password2 == password:
                query = f'''(login,password,birthdate,email)
                VALUES('{login}','{password}','{birthdate}','{email}')'''
                db.insert_one('users',query)
                login_page()
        else:
            print('Пароль не заполнен')
    else:
        print('Поле логин не заполнено')
def to_sql_date(date):
    year = date[len(date)-4:]
    month = date[3:5]
    day = date[0:2]
    sqldate = f'{year}-{month}-{day}'
    print(sqldate)
    return sqldate
def login_page():
    global window
    window = uic.loadUi('auth_form.ui')
    window.auth_button.clicked.connect(auth)#На кнопку входа добавили событие при нажатии
    window.to_reg_button.clicked.connect(to_reg_tab)
    window.show()
def to_reg_tab():
   global window
   window = uic.loadUi('reg_form.ui')
   window.reg_button.clicked.connect(reg)
   window.show()
def get_user():
    global user #Переменная которая будет хранить все поля пользователя
    file = open('user.json','r')#Открывает файл в котором хранится id пользователя
    json_user = json.load(file)#Создаём словарь из файла
    try:
        id = json_user['id']#Получаем id по ключу
        sql_user = db.get_one_by_id('users',id)#Делаем запрос к бд
        if len(sql_user) > 0:#Если данные вернулись создадим пользователя
            user = usermodel.user()
            user.createUser(sql_user)
        else:
            user = None
    except:#При появлении любой ошибки выполнения в try
        print('При получении id произошла ошибка')
        user = None #Зададим пользователя как None
def set_user(id = None):
    file = open('user.json','w')#Открываем файл
    if id != None:#Если id задан указываем этот id как значение
        user = {'id':id}
    else:#Если нет то созадём пустой словарь
        user = {}
    json.dump(user,file)#Записываем наш словарь  
def start_up():
    get_user()
    global user
    if user == None:
        login_page()
    else:
        global window
        window = GeneralUi()


class GeneralUi(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('general.ui')
        self.username = self.ui.label_username
        global user
        self.username.setText(user.login)
        self.ui.exit_button.clicked.connect(self.exit)#Обработка нажатия на кнопку выход
        self.ui.show()
    def exit(self):
        set_user()
        login_page()


start_up()
app.exec()