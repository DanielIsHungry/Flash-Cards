import tkinter as tk
import pickle

def save(name: str, data) -> None: # Not my code
    with open(name, "wb") as file:
        pickle.dump(data, file)

def load(name: str):
    with open(name, "rb") as file:
        return pickle.load(file)
def get_dynamic_font_size(text, base_font_size=30, min_font_size=10, max_font_size=40):
    font_size = base_font_size - len(text) // 5
    font_size = max(min_font_size, min(font_size, max_font_size))
    return font_size

class FlashCards:
    def __init__(self, *args, load=None):
        """
        Initializes Flashcards. Uses args to create an undetermined length.

        Usage:
            (question1, answer1),
            (question2, answer2),
            (question3, answer3)
            or
            load(

        Parameters:
            :param args: all flashcards
            :param load: a saved file
        """
        if load is None:
            self.flashcards = {}
            for arg in args:
                self.flashcards[f'{arg[0]}'] = f'{arg[1]}'
            return
        self.flashcards = load

    def display_current(self, iteration, key_or_val):
        return f'{list(self.flashcards.keys())[iteration]}' if key_or_val == 'key' else f'{list(self.flashcards.items())[iteration][1]}'

    @property
    def length(self):
        return len(self.flashcards)

    def __str__(self):
        return f'{self.flashcards}'

    def save_flashcard(self):
        save(name='flashcards', data=self.flashcards)

    @staticmethod
    def load_flashcard(self):
        load(name='flashcards')


class App(tk.Tk):
    def __init__(self, disable=False, flashcards=None):
        """Initialize Application"""
        super().__init__()

        if disable:
            return

        self.title('Review flashcards')
        self.resizable(True, True)
        self.geometry('900x700')
        self.update_idletasks()

        self.canvas = tk.Canvas(master=self, width=800,
                                height=400, relief=tk.SOLID,
                                borderwidth=5, bg='white',)
        self.canvas.pack(expand=True)

        self.flashcards = flashcards
        self.current_flashcard = 0

        self.show_flashcard()

        self.widgets_frame = tk.Frame(master=self, width=300, height=50, bg='blue')
        self.widgets_frame.pack(pady=100)

        self.previous_button = tk.Button(master=self.widgets_frame, width=20,
                                     height=2, text='Previous Flashcard', font=('Ariel'),
                                     command=self.previous_flashcard)
        self.previous_button.pack(side=tk.LEFT, padx=10)

        self.answer_button = tk.Button(master=self.widgets_frame, width=20,
                                       height=2, text='Show Answer', font=('Ariel'),
                                       command=self.show_answer)
        self.answer_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(master=self.widgets_frame, width=20,
                                     height=2, text='Next Flashcard', font=('Ariel'),
                                     command=self.next_flashcard)
        self.next_button.pack(side=tk.LEFT, padx=10)

        self.mainloop()

    def create_main_text(self, text, font=24):
        """Dynamically create text on the canvas"""
        try:
            if not self.winfo_exists():
                return
        except Exception:
            return
        self.canvas.delete('all')
        self.canvas.create_text(400, 200, text=text, font=('Arial', int(font)), fill='black')

    def show_flashcard(self):
        """Display current flashcard (question or answer)"""
        question = self.flashcards.display_current(self.current_flashcard, 'key')
        self.create_main_text(f'Q: {question}', font=30 - len(question) // 5)

        self.canvas.create_text(160, 25, text=f'Flashcard Number: {self.current_flashcard + 1}', font=('Arial', 24),
                                fill='black')

    def show_answer(self):
        answer = self.flashcards.display_current(self.current_flashcard, 'val')
        font_size = get_dynamic_font_size(answer)  # Get the dynamic font size
        self.create_main_text(f'A: {answer}', font=font_size)

    def next_flashcard(self):
        try:
            self.current_flashcard += 1
            self.show_flashcard()
        except IndexError:
            self.current_flashcard = 0
            self.show_flashcard()

    def previous_flashcard(self):
        try:
            self.current_flashcard -= 1
            self.show_flashcard()
            if self.current_flashcard < 0:
                raise IndexError
        except IndexError:
            self.current_flashcard = flashcards.length - 1
            self.show_flashcard()

if __name__ == '__main__':
    try:
        flashcards = FlashCards(load=load('flashcards'))
        print('From saved file')
        application = App(flashcards=flashcards)
    except FileNotFoundError:
        flashcards = FlashCards(
            ('What is inheritance in Python?',
             'Inheritance allows a class to inherit attributes and methods from another class.'),
            ('What is a constructor in Python?',
             'A constructor is a special method used to initialize objects of a class. In Python, it is defined as __init__.'),
            ('What is polymorphism in Python?',
             'Polymorphism allows different classes to implement the same method, but with different behaviors.'),
            ('What is encapsulation in Python?',
             'Encapsulation is the concept of restricting access to certain details of an object and only exposing necessary functionality.'),
            ('What is abstraction in Python?',
             'Abstraction is the concept of hiding complex implementation details and showing only essential features of an object.'),
            ('What is a class in Python?',
             'A class is a blueprint for creating objects, defining initial state (variables), and behaviors (methods).'),
            ('What is a method in Python?',
             'A method is a function defined within a class that operates on instances of that class.'),
            ('What is the difference between class and instance variables?',
             'Class variables are shared by all instances of a class, while instance variables are unique to each instance of the class.')
        )
        print('New file created')
        flashcards.save_flashcard()
        application = App(flashcards=flashcards)
