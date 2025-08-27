class Question():
    def __init__(self):
        self.text = ''
        self.answers = []
        self.rightAnswerIndex = None
class Test():
    def __init__(self,user):
        self.id = 0
        self.name = ''
        self.description = ''
        self.questions = []
        self.creatorId = user.id #Id создателя
    def add(self,question:Question):
        self.questions.append(question)
    def delete(self,question:Question):
        self.questions.remove(question)