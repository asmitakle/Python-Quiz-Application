import tkinter as tk
from tkinter import messagebox
from tkinter.messagebox import askyesno
from tkinter.simpledialog import askstring
import os, json

THEME_COLOR = "#add8e6"
WIDTH = 900
HEIGHT = 600

class QuizInterface:

    # Constructor to initialize question object
    def __init__(self, quiz_logic):
        self.quiz = quiz_logic
        self.window = tk.Tk()
        self.window.title("Quiz")
        self.window.minsize(WIDTH, HEIGHT)
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_x = (screen_width // 2) - (WIDTH // 2)
        window_y = (screen_height // 2) - (HEIGHT // 2)
        self.window.geometry(f"{self.window.winfo_reqwidth()}x{self.window.winfo_reqheight()}+{window_x}+{window_y}")
        self.window.configure(bg=THEME_COLOR)
        self.window.resizable(False,False)

        # Display Title
        self.display_title()

        # Display question
        self.display_question()

        # Declare a StringVar to store user's answer
        self.user_answer = tk.StringVar()

        # Display four MCQ options
        self.options = self.radio_buttons()
        self.display_options()

        # To show whether the answer is right or wrong
        self.feedback = tk.Label(self.window, bg=THEME_COLOR, font=("ariel", 15, "bold"))
        self.feedback.place(x=0, y=HEIGHT*0.6, relwidth=1, relheight=0.15)

        # Display buttons
        self.buttons()

        # Mainloop
        self.window.mainloop()

    def display_title(self):
        """To display title"""

        title = tk.Label(self.window, text="Quiz Application",
                      bg="#3f51b5", fg="white", font=("ariel", 20, "bold"))

        # place of the title
        title.place(x=0, y=0, relwidth=1, relheight=0.1)

    def display_question(self):
        """To display the question"""

        q_text = self.quiz.next_question()
        question = tk.Label(self.window, text=q_text, anchor='w', bg =THEME_COLOR, 
                            font=("ariel", 15), wraplength=400)
        question.place(x=0, y=HEIGHT*0.1, relwidth=1, relheight=0.2)

    def radio_buttons(self):
        """To create four options (radio buttons)"""

        option_list = []
        y_pos = HEIGHT*0.35

        # adding the options to the list
        while len(option_list) < 4:
            radio_btn = tk.Radiobutton(self.window, text="", variable=self.user_answer,
                                    value='', bg=THEME_COLOR, font=("ariel", 15))

            option_list.append(radio_btn)
            radio_btn.place(x=100, y=y_pos)
            y_pos += HEIGHT*0.05
        
        return option_list

    def display_options(self):
        """To display four options"""

        val = 0
        # deselecting the options
        self.user_answer.set(None)

        # Display text in options
        for option in self.quiz.current_question.options:
            self.options[val]['text'] = option
            self.options[val]['value'] = option
            val += 1

    def submit_btn(self):
        """To check if selected answer is correct"""
        
        user_answer = self.user_answer.get()
        # Check if the answer is correct
        if user_answer == 'None':
            self.feedback["fg"] = "black"
            self.feedback["text"] = f'Skipped.. The correct answer is: {self.quiz.current_question.answer}'
            self.buttons()
        elif self.quiz.check_answer(user_answer):
            self.feedback["fg"] = "green"
            self.feedback["text"] = 'Correct answer!'
            self.buttons()
        else:
            self.feedback['fg'] = 'red'
            self.feedback['text'] = f'Oops! The correct answer is: {self.quiz.current_question.answer}'
            self.buttons()
    
    def next_btn(self):
        """To display next question if there are more questions"""
        
        if self.quiz.has_more_questions():
            # Displays next question with its options
            self.display_question()
            self.display_options()
            # Clear feedback
            self.feedback['fg'] = THEME_COLOR
            self.feedback['text'] = ''
            self.buttons()
        else:
            # If no more questions, displays the score and exits the application
            self.display_result()
            self.window.destroy()
    
    def quit_btn(self):
        """Confirms exit"""
        
        correct, wrong, score_percent = self.quiz.get_score()
        ans = askyesno(title='Confirmation', message=f'You have answered {correct} questions out of {correct+wrong} correctly. \
                       \nYour current score is {score_percent}%. \
                       \nAre you sure you want to quit?')
        if ans:
            self.window.destroy()

    def customize_btn(self):
        """To Modify quiz data"""
      
        try:
            with open('quiz_questions.json', 'r') as data:
                questions = json.load(data)
                total_questions = len(questions)
            
            # Ask for the question number which is to be changed
            q_no = 0
            while not q_no:
                try:
                    q_no = int(askstring(title='Update Data', prompt='What question number do you want to update?'))
                    if q_no > total_questions or q_no < 1:
                        raise ValueError
                except ValueError:
                    messagebox.showinfo(title="Invalid Data", message=f"Please enter an integer in the range 1 to {total_questions}.")
                    q_no = 0
                except TypeError:
                    return
            
            # Ask what part of question is to be changed
            # Changing question text
            if askyesno(title='Update Data', message='Do you want to change the question text?'):
                new_question = askstring(title='Update Data', prompt='Enter new question:')
                questions[q_no-1]['question'] = new_question
            
            # Changing question options
            new_options = questions[q_no-1]['options']
            if askyesno(title='Update Data', message='Do you want to change the options'):
                new_option_1 = askstring(title='Update Data', prompt='Enter option 1:')
                new_option_2 = askstring(title='Update Data', prompt='Enter option 2')
                new_option_3 = askstring(title='Update Data', prompt='Enter option 3')
                new_option_4 = askstring(title='Update Data', prompt='Enter option 4')
                new_options = [new_option_1, new_option_2, new_option_3, new_option_4]
                questions[q_no-1]['options'] = new_options
            
            # Changing correct answer
            if questions[q_no-1]['answer'] not in new_options or askyesno(title='Update Data', message='Do you want to change the correct answer?'):
                new_answer = ''
                while not new_answer:
                    try:
                        new_answer = askstring(title='Update Data', prompt='Enter new correct answer:')
                        if new_answer not in new_options:
                            raise ValueError
                        else:
                            questions[q_no-1]['answer'] = new_answer
                    except ValueError:
                        messagebox.showinfo(title="Invalid Data", message=f"Correct answer should be from one of the options.")
                        new_answer = ''
            
            # Update changes in the data file
            with open('quiz_questions.json', 'w') as data:
                json.dump(questions, data, indent=4)
                
        except json.JSONDecodeError:
            print("Invalid JSON data")
    
        # Reload the quiz
        self.window.destroy()
        with open(os.path.join('./', 'main.py'), 'r') as file:
            exec(file.read())


    def buttons(self):
        """To display buttons"""
        # Toggle between Submit and Next buttons
        if self.feedback['text'] == '':
            submit_button = tk.Button(self.window, text="Submit", command=self.submit_btn,
                                bg="green", fg="white", font=("ariel", 16, "bold"))
            submit_button.place(x=0, y=HEIGHT*0.75, relwidth=0.48)
        else:
            next_button = tk.Button(self.window, text="Next", command=self.next_btn,
                                bg="orange", fg="white", font=("ariel", 16, "bold"))
            next_button.place(x=0, y=HEIGHT*0.75, relwidth=0.48)
        
        quit_button = tk.Button(self.window, text="Quit", command=self.quit_btn,
                             bg="red", fg="white", font=("ariel", 16, " bold"))
        quit_button.place(x=WIDTH*1/2, y=HEIGHT*0.75, relwidth=0.48)

        customize_quiz_button = tk.Button(self.window, text="Customize this Quiz", command=self.customize_btn,
                             bg="blue", fg="white", font=("ariel", 16, " bold"))
        customize_quiz_button.place(x=0, y=HEIGHT*0.85, relwidth=0.98)

    def display_result(self):
        """To display the result using messagebox"""
        correct, wrong, score_percent = self.quiz.get_score()

        correct = f"Correct: {correct}"
        wrong = f"Wrong: {wrong}"

        # calculates score percentage
        result = f"Score: {score_percent}%"

        # Shows a message box to display the result
        messagebox.showinfo("Result", f"{result}\n{correct}\n{wrong}")