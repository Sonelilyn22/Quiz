from PyQt6 import QtWidgets,uic
import db
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
    login =  window.input_login.text()
    password = window.input_pass.text()
    if login != '':
        if password!='':
            query = f'''login = '{login}' and password = '{password}' '''
            print(query)
            result = db.get_one_by_filter('users',query)
            print(result)
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

login_page()
app.exec()