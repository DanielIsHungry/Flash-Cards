import tkinter as tk
import pickle
from tkinter import messagebox

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
        return load(name='flashcards')

class FlashcardMaker(tk.Toplevel):
    def __init__(self, app, flashcards):
        super().__init__()

        self.app = app
        self.flashcards = flashcards

        self.title('Flashcard Maker')
        self.update_idletasks()
        self.geometry(f'800x{self.winfo_screenheight() - 100}+0+0')
        self.minsize(650, 0)
        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.label = tk.Label(scrollable_frame, text='YOUR FLASHCARDS:\nNone', wraplength=300, justify='left')
        self.label.pack(pady=20, padx=20, anchor="w")

        add_new_button = tk.Button(self, text='Add new flashcard', font=('Ariel', 15), relief=tk.GROOVE, command=self.add_new_flashcard)
        add_new_button.pack(padx=20, pady=20)

        remove_flashcard = tk.Button(self, text='Remove a flashcard', font=('Ariel', 15), relief=tk.GROOVE, command=self.remove_flashcard)
        remove_flashcard.pack(padx=20, pady=20)

        remove_all_button = tk.Button(self, text='Remove all flashcards', font=('Ariel', 15), relief=tk.GROOVE, command=self.remove_all)
        remove_all_button.pack(padx=20, pady=20)

        save_and_close_button = tk.Button(self, text='Load a save', font=('Ariel', 15), relief=tk.GROOVE, command=self.load_saved_flashcards)
        save_and_close_button.pack(padx=20, pady=20)

        save_and_close_button = tk.Button(self, text='Save current flashcards', font=('Ariel', 15), relief=tk.GROOVE, command=self.save_current_flashcards)
        save_and_close_button.pack(padx=20, pady=20)

        save_and_close_button = tk.Button(self, text='Save and close', font=('Ariel', 15), relief=tk.GROOVE, command=lambda: self.destroy())
        save_and_close_button.pack(padx=20, pady=20)

        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        self.edit_warplength()
        self.update_flashcard_display()

    def remove_all(self):
        confirm = messagebox.askyesno('Remove all?', 'Would you like to remoove all of your current flashcards?')

        if confirm:
            self.flashcards.flashcards = {}
            messagebox.showinfo('', 'All flashcards deleted!')
            self.lift()

            self.update_flashcard_display()
            self.update_app_cards()
            return
        return


    def add_new_flashcard(self):
        win = tk.Toplevel(self)
        win.geometry('400x300')
        win.title('Add new flashcard')
        win.resizable(False, False)

        ql = tk.Label(win, text='What will be the flashcard question?', font=('Ariel', 10))
        ql.pack(pady=10)

        qe = tk.Entry(win, width=30, font=('Ariel', 15))
        qe.pack(pady=20)

        al = tk.Label(win, text='What will be the flashcard answer?', font=('Ariel', 10))
        al.pack(pady=10)

        ae = tk.Entry(win, width=30, font=('Ariel', 15))
        ae.pack(pady=20)

        def submit_data():
            question = qe.get().strip()
            answer = ae.get().strip()

            if question and answer:
                self.flashcards.flashcards[question] = answer
                self.flashcards.save_flashcard()
                self.update_flashcard_display()

                self.update_app_cards()

                win.destroy()

        submit = tk.Button(win, text='Submit data', relief=tk.GROOVE, font=('Ariel', 15), command=submit_data)
        submit.pack()

    def remove_flashcard(self):
        """Remove a flashcard by selecting its number, ofc."""
        if not self.flashcards.flashcards:
            return

        win = tk.Toplevel(self)
        win.geometry('400x200')
        win.title('Remove Flashcard')
        win.resizable(False, False)

        tk.Label(win, text='Select flashcard number to remove:', font=('Ariel', 10)).pack(pady=10)

        flashcard_numbers = list(range(1, len(self.flashcards.flashcards) + 1))
        selected_flashcard = tk.StringVar(win)
        selected_flashcard.set(flashcard_numbers[0])

        dropdown = tk.OptionMenu(win, selected_flashcard, *flashcard_numbers)
        dropdown.pack(pady=20)

        def submit_removal():
            try:
                index = int(selected_flashcard.get()) - 1
                question_to_remove = list(self.flashcards.flashcards.keys())[index]

                del self.flashcards.flashcards[question_to_remove]
                self.flashcards.save_flashcard()

                self.update_app_cards()

                self.update_flashcard_display()
                win.destroy()
            except Exception as e:
                tk.Label(win, text=f"Error: {e}", fg="red").pack()

        submit = tk.Button(win, text='Remove', relief=tk.GROOVE, font=('Ariel', 15), command=submit_removal)
        submit.pack()

    def edit_warplength(self):
        wrap_length = self.winfo_width() - 300
        self.label.config(wraplength=wrap_length)
        self.after(10, self.edit_warplength)

    def load_save(self, name: str):
        self.flashcards.flashcards = load(f'{name}')
        self.update_app_cards()
        self.update_flashcard_display()

    def update_flashcard_display(self):
        if len(self.flashcards.flashcards) == 0:
            self.label.config(text=f'YOUR FLASHCARDS:\nNothing to see here! Click \'Add flashcard\' to get started!')
        flashcard_texts = [
            f'Flashcard Number: {i + 1}\n\nQuestion: {q}\n\nAnswer: {a}\n\n------\n'
            for i, (q, a) in enumerate(self.flashcards.flashcards.items())
        ]
        keys_text = "\n\n".join(flashcard_texts)
        self.label.config(text=f'YOUR FLASHCARDS:\n{keys_text}')

    def update_app_cards(self):
        self.app.update_flashcards(self.flashcards)

    def load_saved_flashcards(self):
        win = tk.Toplevel(self)
        win.geometry('400x200')
        win.title('Load saved flashcards')
        win.resizable(False, False)

        nl = tk.Label(win, text='Enter the file name to load', font=('Ariel', 10))
        nl.pack(pady=20)

        ne = tk.Entry(win, width=30, font=('Ariel', 10))
        ne.pack(pady=20)

        def submit_data():
            try:
                self.flashcards.flashcards = dict(load(f'{ne.get()}'))
                messagebox.showinfo('', 'Set of flashcards successfuly loaded!')
                self.lift()
                self.update_flashcard_display()
                self.update_app_cards()
            except Exception as e:
                messagebox.showerror('', f'Set of flashcards failed to load.\n{e}')

        submit = tk.Button(win, text='Load set', command=submit_data, font=('Ariel', 10))
        submit.pack(pady=20)

    def save_current_flashcards(self):
        win = tk.Toplevel(self)
        win.geometry('400x200')
        win.title('Save current flashcards')
        win.resizable(False, False)

        nl = tk.Label(win, text='Enter the name you would like to save the file', font=('Ariel', 10))
        nl.pack(pady=20)

        ne = tk.Entry(win, width=30, font=('Ariel', 10))
        ne.pack(pady=20)

        def submit_data():
            save(name=f'{ne.get()}', data=self.flashcards.flashcards)

        submit = tk.Button(win, text='Save', command=submit_data, font=('Ariel', 10))
        submit.pack(pady=20)



class App(tk.Tk):
    def __init__(self, disable=False, flashcards=FlashCards((None, None))):
        """Initialize Application"""
        super().__init__()

        if disable:
            return

        self.title('Review flashcards')
        self.resizable(True, True)
        self.geometry('1000x700+0+0')
        self.update_idletasks()

        self.canvas = tk.Canvas(self, width=800, height=400, relief=tk.SOLID, borderwidth=5, bg='white',)
        self.canvas.pack(expand=True)

        self.flashcards = flashcards
        self.current_flashcard = 0

        self.show_flashcard()

        self.widgets_frame = tk.Frame(self, width=300, height=50)
        self.widgets_frame.pack(pady=100)

        self.previous_button = tk.Button(self.widgets_frame, width=20, height=2, text='Previous Flashcard', font=('Ariel'), command=self.previous_flashcard, relief=tk.GROOVE)
        self.previous_button.pack(side=tk.LEFT, padx=10)

        self.answer_button = tk.Button(self.widgets_frame, width=20, height=2, text='Show Answer', font=('Ariel'), command=self.show_answer, relief=tk.GROOVE)
        self.answer_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(self.widgets_frame, width=20, height=2, text='Next Flashcard', font=('Ariel'), command=self.next_flashcard, relief=tk.GROOVE)
        self.next_button.pack(side=tk.LEFT, padx=10)

        self.debug = tk.Button(self.widgets_frame, width=20, height=2, text='Edit flashcards', font=('Ariel'), command=lambda: FlashcardMaker(flashcards=self.flashcards, app=self), relief=tk.GROOVE)
        self.debug.pack(side=tk.LEFT, padx=10)

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

        self.canvas.create_text(160, 25, text=f'Flashcard Number: {self.current_flashcard + 1}', font=('Arial', 24), fill='black')

    def show_answer(self):
        answer = self.flashcards.display_current(self.current_flashcard, 'val')
        font_size = get_dynamic_font_size(answer)
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
            self.current_flashcard = self.flashcards.length - 1
            self.show_flashcard()

    def update_flashcards(self, flashcards):
        self.flashcards = flashcards

if __name__ == '__main__':
    App()
