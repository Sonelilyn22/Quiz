
from PyQt6 import QtWidgets

class CreateQuestionUi(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.answers = [] #Список с lineEdit 
        self.mainLayot = QtWidgets.QVBoxLayout() #Общий verticalLayout
        self.lineEditLayout = QtWidgets.QVBoxLayout() #Layout для ответов
        self.label= QtWidgets.QLabel('Название')
        self.textField = QtWidgets.QLineEdit() #Поле для названия вопроса
        self.textField.setPlaceholderText('Введите название вопроса')
        self.button = QtWidgets.QPushButton('Добавить вопрос')
        self.button.clicked.connect(self.setlineedit)
        self.rightAnswer = QtWidgets.QComboBox()
        self.mainLayot.addWidget(self.label)
        self.mainLayot.addWidget(self.textField)
        self.mainLayot.addWidget(self.button)
        self.mainLayot.addLayout(self.lineEditLayout)
        self.mainLayot.addWidget(QtWidgets.QLabel('Правильный ответ'))
        self.mainLayot.addWidget(self.rightAnswer)
        self.setlineedit()
        self.setLayout(self.mainLayot)
        self.show()
    def setlineedit(self):
        lineEdit = QtWidgets.QLineEdit()
        lineEdit.textChanged.connect(self.setRightAnsewerText)
        self.answers.append(lineEdit)
        self.lineEditLayout.addWidget(lineEdit)
    def setRightAnsewerText(self):
        self.rightAnswer.clear()
        for element in self.answers:
            self.rightAnswer.addItem(element.text())