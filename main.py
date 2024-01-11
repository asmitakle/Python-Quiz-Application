from quizData import loadQuizData
from quizLogic import QuizLogic
from quizUI import QuizInterface

question_bank = loadQuizData()
quiz = QuizLogic(question_bank)
quiz_ui = QuizInterface(quiz)