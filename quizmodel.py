class Question():
    def __init__(self):
        self.id = None
        self.text = ''
        self.answers = []
        self.rightAnswerIndex = None
    def create(self,sql_question:list):
        self.id = sql_question[0]
        self.text = sql_question[1]
        for answer in sql_question[2]:
            self.answers.append(answer)
        self.rightAnswerIndex = sql_question[3]
class Test():
    def __init__(self,user):
        self.id = None
        self.name = ''
        self.description = ''
        self.questions = [] 
        self.creatorId = user.id #Id создателя
    def add(self,question:Question):
        self.questions.append(question)
    def delete(self,question:Question):
        self.questions.remove(question)