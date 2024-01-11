import json
from random import shuffle
from questionStructure import Question

def loadQuizData(data_file = 'quiz_questions.json'):
    """Loads data from JSON file into program"""
    
    questions = []
    try:
        with open(data_file, 'r') as data:
            questions = json.load(data)
    except json.JSONDecodeError:
        print("Invalid JSON data")
    
    question_bank = []
    for question in questions:
        options_list = []
        question_text = question["question"]
        options = question["options"]
        answer = question["answer"]
        for option in options:
            options_list.append(option)
        shuffle(options_list)
        new_question = Question(question_text, options_list, answer)
        question_bank.append(new_question)
    
    return question_bank

        

# import requests

# parameters = {
#     "amount": 10,
#     "type": "multiple"
# }

# response = requests.get(url="https://opentdb.com/api.php", params=parameters)
# questions = response.json()["results"]
 
# # Data to be written
# questions = [
#     {
#         "question": "What is the capital of France?",
#         "options": ["Paris", "Berlin", "Madrid", "Rome"],
#         "answer": "Paris"
#     },
#     {
#         "question": "What is the capital of Germany?",
#         "options": ["Berlin", "London", "Paris", "Rome"],
#         "answer": "Berlin"
#     },
#     {
#         "question": "What is the capital of Italy?",
#         "options": ["Rome", "Madrid", "Berlin", "Paris"],
#         "answer": "Rome"
#     }
# ]
 
# with open('default_questions.json', 'w') as f:
#     json.dump(questions, f, indent=4)