"""
    This script file contains the GUI logic for the application. The application uses Tkinter to handle the GUI
    and matplotlib to display a pie chart of the user's data.
"""
import random
import re
import tkinter as tk
import tkinter.messagebox
from datetime import datetime
from tkinter import messagebox
from tkinter import ttk

import matplotlib.pyplot as plt
import sqlalchemy.exc
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from database.enumerations import Mood
from wellness_service.financial_wellness import insert_financial_wellness_data, get_all_financial_wellness_data, \
    get_financial_wellness_data, update_financial_wellness_data
from wellness_service.journal import get_journal_logs, insert_journal_log, update_journal, get_journal_by_date
from wellness_service.mindfulness import insert_mindfulness_log, get_mindfulness_data_history, get_mindfulness_data, \
    update_mindfulness_data
from wellness_service.wellness_visual import show_financial_wellness_pie_chart, show_mood_wellness_pie_chart, \
    show_mood_wellness_pie_chart_date_filter, show_financial_wellness_by_date

# Wellness Quotes to be used by the Mindfulness page
WELLNESS_QUOTES = [
    "For I know the plans I have for you, declares the Lord,\n "
    "plans to prosper you and not harm you, \nplans to give you hope and a future -Jeremiah 29:11",
    "A friend loves at all times. -Proverbs 17:17",
    "Mercy, onto you, and peace and love be multiplied -Jude 1:2",
    "The LORD is my shepard, I lack nothing.\n He makes me lie down in green pastures\n"
    "\nHe leads me beside quiet waters,\n he refreshes my soul - Psalm 23 1:3"
]


class WellnessApp(tk.Tk):
    """
        The top level class representing the main window of the application assigns all of the frames and
        assists with the transitioning of frames
    """

    def __init__(self):
        super().__init__()

        self.title("Wellness Services")
        self.geometry("950x650")

        container = ttk.Frame(self)
        # the fill option tells the manager that the widget should fill the whole space
        # Both means that the widget expands vertically and horizontally
        # Expand tells the manager to assign additional space to the widget box.
        container.pack(fill="both", expand=True)

        # Add all the frames to the frames dictionary. This helps to navigate between frames
        self.frames = {}
        for F in (WelcomeScreen, FinancialScreen, DisplayFinancesScreen, UpdateFinancesScreen, MindfulScreen,
                  DisplayMindfulnessScreen, UpdateMindfulnessScreen, JournalScreen, DisplayJournalsScreen,
                  UpdateJournalScreen):
            page_name = F.__name__
            # The parent is the parent of the frame (the main window) and controller acts as a common point
            # of interaction
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # When the application starts show the Welcome Screen
        self.show_frame("WelcomeScreen")

    def show_frame(self, page_name):
        """
            show_frame() uses the tkraise() function to raise the given page making it viewable
        """
        frame = self.frames[page_name]
        frame.tkraise()

    def get_frame(self, page_name):
        """
             get_frame() returns the frame name for the update screens
        """
        return self.frames[page_name]


def validate_date_for_create(date_str):
    """
    validate_date_for_create function used to validate dates across the application
    If the user tries to make a new record on the same day, the application will tell them to
    go to the Log History page by clicking on the Log History button
    """
    # Check if the date string matches the format YYYY-MM-DD
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            if get_financial_wellness_data(date_str):
                tkinter.messagebox.showinfo(title="Existing Record Warning", message="There is an existing record under"
                                                                                     " this date\n To update the record"
                                                                                     " for this date click on the Log "
                                                                                     " History button"
                                            )
            return True
        except ValueError:
            return False
    return False


def validate_date_filter(date_str):
    """
    This function validates the date format on the date filters
    :param date_str:
    :return:
    """
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            tkinter.messagebox.showinfo("Invalid Input", "Date must be in YYYY-MM-DD format")
            return False
    else:
        tkinter.messagebox.showerror("Invalid Input", "Date must be in YYYY-MM-DD format")
        return False


class WelcomeScreen(ttk.Frame):
    """
        WelcomeScreen describes the Welcome Screen frame.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Which wellness service would you like to use?")
        # 'pady' pads externally along the y-axis
        # similarly 'padx' pads extermnally along the x-axis
        label.pack(pady=10)

        # When user clicks on this button, they are taken to the Financial Screen
        financial_button = ttk.Button(self, text="Financial",
                                      command=lambda: controller.show_frame("FinancialScreen"))
        financial_button.pack(pady=10)

        # When the user clicks this button, they are taken to the Mindful Screen
        mindfulness_button = ttk.Button(self, text="Mindfulness",
                                        command=lambda: controller.show_frame("MindfulScreen"))
        mindfulness_button.pack(pady=10)


class FinancialScreen(ttk.Frame):
    """
        FinancialScreen describes the Financial Screen Frame
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.create_widgets()
        self.display_finances()

    def create_widgets(self):
        """
        create_widgets is a function called when the frame is first initiated
        It places the widgets within the frame
        :return:
        """
        ttk.Label(self, text="Date (YYYY-MM-DD)*").grid(row=0, column=0, pady=10, padx=10)
        self.date_entry = ttk.Entry(self, validate='focusout',
                                    validatecommand=(self.register(validate_date_for_create), '%P'))
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.date_entry.grid(row=0, column=1, pady=10, padx=10)

        ttk.Label(self, text="Income*").grid(row=1, column=0, pady=10, padx=10)
        self.income_entry = ttk.Entry(self)
        self.income_entry.grid(row=1, column=1, pady=10, padx=10)

        ttk.Label(self, text="Grocery Expense*").grid(row=2, column=0, pady=10, padx=10)
        self.grocery_entry = ttk.Entry(self)
        self.grocery_entry.grid(row=2, column=1, pady=10, padx=10)

        ttk.Label(self, text="Utility Expense*").grid(row=3, column=0, pady=10, padx=10)
        self.utility_entry = ttk.Entry(self)
        self.utility_entry.grid(row=3, column=1, pady=10, padx=10)

        ttk.Label(self, text="Rent Expense*").grid(row=4, column=0, pady=10, padx=10)
        self.rent_entry = ttk.Entry(self)
        self.rent_entry.grid(row=4, column=1, pady=10, padx=10)

        ttk.Label(self, text="Food Expense*").grid(row=5, column=0, pady=10, padx=10)
        self.food_entry = ttk.Entry(self)
        self.food_entry.grid(row=5, column=1, pady=10, padx=10)

        ttk.Label(self, text="Misc Expense*").grid(row=6, column=0, pady=10, padx=10)
        self.misc_entry = ttk.Entry(self)
        self.misc_entry.grid(row=6, column=1, pady=10, padx=10)

        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=7, pady=10, padx=10)

        back_button = ttk.Button(self, text="Back to Welcome",
                                 command=lambda: self.controller.show_frame("WelcomeScreen"))
        back_button.grid(row=7, column=0, pady=10, padx=10)

        submit_finances_button = ttk.Button(self, text="Submit",
                                            command=lambda: self.submit_finances_pressed())
        submit_finances_button.grid(row=7, column=1, pady=10, padx=10)
        display_finances_button = ttk.Button(self, text="Log History",
                                             command=lambda: self.controller.show_frame("DisplayFinancesScreen"))
        display_finances_button.grid(row=7, column=2, pady=10, padx=10)
        ttk.Label(self, text="Start Date (YYYY-MM-DD)*").grid(row=8, column=0, pady=10, padx=10)
        self.start_date_entry = ttk.Entry(self, validate='focusout',
                                          validatecommand=(self.register(validate_date_filter)
                                                           , '%P'))
        self.start_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.start_date_entry.grid(row=8, column=1, pady=10, padx=10)

        ttk.Label(self, text="End Date (YYYY-MM-DD)*").grid(row=9, column=0, pady=10, padx=10)
        self.end_date_entry = ttk.Entry(self, validate='focusout', validatecommand=(self.register(validate_date_filter),
                                                                                    '%P'))
        self.end_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.end_date_entry.grid(row=9, column=1, pady=10, padx=10)

        get_financial_data_between_dates_btn = ttk.Button(self, text="Fill Pie Chart With Data Between Dates",
                                                          command=lambda: self.display_finances_date_filter())
        get_financial_data_between_dates_btn.grid(row=8, column=2, padx=10, pady=10)

    def submit_finances_pressed(self):
        """
        the function called when the user presses the submit button
        :return:
        """
        if self.validate_inputs():
            try:

                insert_financial_wellness_data(float(self.income_entry.get()),
                                               float(self.grocery_entry.get()),
                                               float(self.utility_entry.get()),
                                               float(self.rent_entry.get()),
                                               float(self.food_entry.get()),
                                               float(self.misc_entry.get()),
                                               datetime.strptime(self.date_entry.get(), '%Y-%m-%d').date())
                tkinter.messagebox.showinfo(title="Success", message="Saved Successfully")

                self.display_finances()
            except sqlalchemy.exc.SQLAlchemyError:
                tkinter.messagebox.showinfo(title="Failure", message="Cannot save two records for the same day\n"
                                                                     "Click on the Log History button to locate your"
                                                                     " record")

    def display_finances(self):
        """
        This function displays the pie chart on the frame. It returns a pie chart containing
         all the financial data that the user has put in
        :return:
        """
        # clear the previous plot
        self.figure.clear()
        # plot the new pie chart
        show_financial_wellness_pie_chart(self.figure)
        # update the canvas
        self.canvas.draw()

    def display_finances_date_filter(self):
        """
        this function displays the pie chart on the frame with an added filter for select dates
        :return:
        """
        if self.start_date_entry.get() != '' and self.end_date_entry.get() != '':
            self.figure.clear()
            show_financial_wellness_by_date(self.figure,
                                            datetime.strptime(self.start_date_entry.get(), "%Y-%m-%d").date(),
                                            datetime.strptime(self.end_date_entry.get(), "%Y-%m-%d").date())
            self.canvas.draw()

    def tkraise(self, aboveThis=None):
        """
        This overrides the tkraise function to refresh the pie chart every time the frame is raised
        :param aboveThis:
        :return:
        """
        super().tkraise(aboveThis)
        self.display_finances()

    def validate_inputs(self):
        """
        Input validation for the frame. This is called when the user presses the submit button
        :return:
        """
        date_entry = self.date_entry.get()
        income = self.income_entry.get()
        grocery = self.grocery_entry.get()
        utility = self.utility_entry.get()
        rent = self.rent_entry.get()
        food = self.food_entry.get()
        misc = self.misc_entry.get()

        try:
            datetime.strptime(date_entry, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Invalid Input", "Date must be in YYYY-MM-DD format")
            return False

        if not income or not grocery or not utility or not rent or not food or not misc:
            messagebox.showerror("Invalid Input", "All fields must be filled")
            return False

        try:
            float(income)
            float(grocery)
            float(utility)
            float(rent)
            float(food)
            float(misc)
        except ValueError:
            messagebox.showerror("Invalid Input", "Expenses and Income must be numbers")
            return False

        return True


class DisplayFinancesScreen(ttk.Frame):
    """
    This class describes the Display Finances Screen
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        """
        The create widgets function creates and places the widgets within the frame
        :return:
        """
        self.instruction_label = ttk.Label(self, text="Click on the date to open the log")
        self.instruction_label.pack(padx=10, pady=10)

        self.finance_listbox = tk.Listbox(self)
        self.finance_listbox.pack(fill="both", expand=True, pady=10, padx=10)

        for finance in get_all_financial_wellness_data():
            self.finance_listbox.insert(tk.END, finance.log_date)

        self.finance_listbox.bind("<<ListboxSelect>>", self.on_select)

        back_button = ttk.Button(self, text="Back to Financial",
                                 command=lambda: self.controller.show_frame("FinancialScreen"))
        back_button.pack(pady=10)

    def on_select(self, event):
        """
        event for when the user clicks on an item within the ListBox
        :param event:
        :return:
        """
        selected_index = self.finance_listbox.curselection()
        if selected_index:
            selected_date = self.finance_listbox.get(selected_index)
            finance = get_financial_wellness_data(selected_date)
            update_frame = self.controller.get_frame("UpdateFinancesScreen")
            # remove all the data that may be in the frame and repopulate it with the
            # finance log's data
            update_frame.date_entry.delete(0, tk.END)
            update_frame.date_entry.insert(0, finance.log_date)
            update_frame.date_entry.config(state=tk.DISABLED)

            update_frame.income_entry.delete(0, tk.END)
            update_frame.income_entry.insert(0, finance.income)

            update_frame.grocery_entry.delete(0, tk.END)
            update_frame.grocery_entry.insert(0, finance.grocery_expense)

            update_frame.utility_entry.delete(0, tk.END)
            update_frame.utility_entry.insert(0, finance.utility_expense)

            update_frame.rent_entry.delete(0, tk.END)
            update_frame.rent_entry.insert(0, finance.rent)

            update_frame.food_entry.delete(0, tk.END)
            update_frame.food_entry.insert(0, finance.food_expense)

            update_frame.misc_entry.delete(0, tk.END)
            update_frame.misc_entry.insert(0, finance.misc_expense)

            self.controller.show_frame("UpdateFinancesScreen")

    def clear_widgets(self):
        """
        clear widgets is used for removing all widgets from the frame
        This function is necessary for the page data to be updated
        :return:
        """
        for widget in super().winfo_children():
            widget.destroy()

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.clear_widgets()
        self.create_widgets()


class UpdateFinancesScreen(ttk.Frame):
    """
        class describing the Update Finances Screen Frame
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.create_widgets()

    def create_widgets(self):
        """
        Creates and displays the widgets for the Update Finances Screen Frame
        :return:
        """
        ttk.Label(self, text="Date (YYYY-MM-DD)").grid(row=0, column=0, pady=10, padx=10)
        self.date_entry = ttk.Entry(self)
        self.date_entry.grid(row=0, column=1, pady=10, padx=10)

        ttk.Label(self, text="Income").grid(row=1, column=0, pady=10, padx=10)
        self.income_entry = ttk.Entry(self)
        self.income_entry.grid(row=1, column=1, pady=10, padx=10)

        ttk.Label(self, text="Grocery Expense").grid(row=2, column=0, pady=10, padx=10)
        self.grocery_entry = ttk.Entry(self)
        self.grocery_entry.grid(row=2, column=1, pady=10, padx=10)

        ttk.Label(self, text="Utility Expense").grid(row=3, column=0, pady=10, padx=10)
        self.utility_entry = ttk.Entry(self)
        self.utility_entry.grid(row=3, column=1, pady=10, padx=10)

        ttk.Label(self, text="Rent Expense").grid(row=4, column=0, pady=10, padx=10)
        self.rent_entry = ttk.Entry(self)
        self.rent_entry.grid(row=4, column=1, pady=10, padx=10)

        ttk.Label(self, text="Food Expense").grid(row=5, column=0, pady=10, padx=10)
        self.food_entry = ttk.Entry(self)
        self.food_entry.grid(row=5, column=1, pady=10, padx=10)

        ttk.Label(self, text="Misc Expense").grid(row=6, column=0, pady=10, padx=10)
        self.misc_entry = ttk.Entry(self)
        self.misc_entry.grid(row=6, column=1, pady=10, padx=10)

        submit_button = ttk.Button(self, text="Submit",
                                   command=lambda: self.submit_finance_update())
        submit_button.grid(row=7, column=0, pady=10, padx=10)

        close_button = ttk.Button(self, text="Close",
                                  command=lambda: self.controller.show_frame("DisplayFinancesScreen"))
        close_button.grid(row=7, column=1, pady=10, padx=10)

    def submit_finance_update(self):
        """
        Function called when the user clicks the submit button on the page
        :return:
        """
        if self.validate_inputs():
            try:
                update_financial_wellness_data(float(self.income_entry.get()),
                                               float(self.grocery_entry.get()),
                                               float(self.utility_entry.get()),
                                               float(self.rent_entry.get()),
                                               float(self.food_entry.get()),
                                               float(self.misc_entry.get()),
                                               datetime.strptime(self.date_entry.get(), '%Y-%m-%d').date())
                tkinter.messagebox.showinfo(title="Success", message="Saved Successfully")

            except sqlalchemy.exc.SQLAlchemyError:
                tkinter.messagebox.showinfo(title="Error", message="Error saving the update")

    def validate_inputs(self):
        """
        Input validation for the page. This is only called when the user presses the submit button
        :return:
        """
        income = self.income_entry.get()
        grocery = self.grocery_entry.get()
        utility = self.utility_entry.get()
        rent = self.rent_entry.get()
        food = self.food_entry.get()
        misc = self.misc_entry.get()

        if not income or not grocery or not utility or not rent or not food or not misc:
            messagebox.showerror("Invalid Input", "All fields must be filled")
            return False

        try:
            float(income)
            float(grocery)
            float(utility)
            float(rent)
            float(food)
            float(misc)
        except ValueError:
            messagebox.showerror("Invalid Input", "Expenses and Income must be numbers")
            return False

        return True


class MindfulScreen(ttk.Frame):
    """
    This class describes the Mindful Screen Frame.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        self.display_moods()

    def create_widgets(self):
        """
        This function creates the widgets for the Mindful Screen
        :return:
        """
        random_quote = random.choice(WELLNESS_QUOTES)
        self.quote_label = ttk.Label(self, text=random_quote)
        self.quote_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        # New Date Entry
        ttk.Label(self, text="Date (YYYY-MM-DD)").grid(row=1, column=0, pady=10, padx=10)
        self.date_entry = ttk.Entry(self, validate='focusout', validatecommand=(self.register(validate_date_for_create)
                                                                                , '%P'))
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.date_entry.grid(row=1, column=1, pady=10, padx=10)

        ttk.Label(self, text="How is your mood?").grid(row=2, column=0, pady=10, padx=10)
        self.mood_var = tk.StringVar()
        self.mood_dropdown = ttk.Combobox(self, textvariable=self.mood_var, state='readonly')
        self.mood_dropdown['values'] = [e.value for e in Mood]
        self.mood_dropdown.grid(row=2, column=1, pady=10, padx=10)

        submit_mood_btn = ttk.Button(self, text="Submit",
                                     command=lambda: self.submit_mood())
        submit_mood_btn.grid(row=3, column=1, pady=10, padx=10)

        ttk.Label(self, text="Start Date (YYYY-MM-DD)").grid(row=4, column=0, pady=10, padx=10)
        self.start_date_entry = ttk.Entry(self, validate='focusout',
                                          validatecommand=(self.register(validate_date_filter), '%P'))
        self.start_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.start_date_entry.grid(row=4, column=1, pady=10, padx=10)

        ttk.Label(self, text="End Date (YYYY-MM-DD)").grid(row=5, column=0, pady=10, padx=10)
        self.end_date_entry = ttk.Entry(self, validate='focusout',
                                        validatecommand=(self.register(validate_date_filter), '%P'))
        self.end_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.end_date_entry.grid(row=5, column=1, pady=10, padx=10)

        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=4, pady=10, padx=10)

        display_mindfulness_button = ttk.Button(self, text="Log History",
                                                command=lambda: self.controller.show_frame("DisplayMindfulnessScreen"))
        display_mindfulness_button.grid(row=8, column=1, pady=10, padx=10)

        display_mood_chart_between_dates_btn = ttk.Button(self, text="Display mood chart between dates",
                                                          command=lambda: self.display_moods_between_dates())
        display_mood_chart_between_dates_btn.grid(row=7, column=1, pady=10, padx=10)

        journal_button = ttk.Button(self, text="Journal",
                                    command=lambda: self.controller.show_frame("JournalScreen"))
        journal_button.grid(row=6, column=2, pady=10, padx=10)

        back_button = ttk.Button(self, text="Back to Welcome",
                                 command=lambda: self.controller.show_frame("WelcomeScreen"))
        back_button.grid(row=7, column=2, pady=10, padx=10)

    def submit_mood(self):
        """
        The function called when the user presses the submit button
        :return:
        """
        if self.validate_input():
            try:
                insert_mindfulness_log(self.mood_var.get(), datetime.strptime(self.date_entry.get(), "%Y-%m-%d").date())
                tkinter.messagebox.showinfo(title="Success", message="Mood Saved")
                self.display_moods()
            except sqlalchemy.exc.SQLAlchemyError:
                tkinter.messagebox.showinfo(title="Error",
                                            message="Cannot save over current date, to change today's mood"
                                                    "\n click the Display Moods button")

    def display_moods(self):
        """
        This function displays the mood pie chart of all the entries the user has entered
        :return:
        """
        self.figure.clear()
        # plot the new pie chart
        show_mood_wellness_pie_chart(self.figure)
        # update the canvas
        self.canvas.draw()

    def display_moods_between_dates(self):
        """
        This function displays the mood pie chart of all the entries between two dates
        :return:
        """

        if self.start_date_entry.get() == '' or self.end_date_entry.get() == '':
            tkinter.messagebox.showinfo(title="Error", message="Please enter dates to be searched")
        else:
            self.figure.clear()
            show_mood_wellness_pie_chart_date_filter(self.figure,
                                                     datetime.strptime(self.start_date_entry.get(), "%Y-%m-%d").date(),
                                                     datetime.strptime(self.end_date_entry.get(), "%Y-%m-%d").date())
            # update the canvas
            self.canvas.draw()

    def replace_quote_label(self):
        """
        This function replaces the quote label every time the user re-navigates to the page
        :return:
        """
        self.quote_label.config(text=random.choice(WELLNESS_QUOTES))

    def tkraise(self, aboveThis=None):
        """
        This function overrides the tkraise function to be called whenever the frame is raised
        :param aboveThis:
        :return:
        """
        super().tkraise(aboveThis)
        self.replace_quote_label()
        self.display_moods()

    def validate_input(self):
        """
        This function validates the input of the user when the user presses the submit button
        :return:
        """
        mood = self.mood_var.get()
        date_entry = self.date_entry.get()
        if not mood or not date_entry:
            messagebox.showinfo(title="Error", message="The mood and date inputs must be filled")
            return False
        return validate_date_filter(date_entry)


class DisplayMindfulnessScreen(ttk.Frame):
    """
    This class describes the Display Mindfulness Screen Frame
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        """
        This function creates the widgets for the DisplayMindfulnessScreen
        :return:
        """

        self.instruction_label = ttk.Label(self, text="Click on the date to open the log")
        self.instruction_label.pack(padx=10, pady=10)

        self.mindfulness_listbox = tk.Listbox(self)
        self.mindfulness_listbox.pack(fill="both", expand=True, pady=10, padx=10)

        for mindful in get_mindfulness_data_history():
            self.mindfulness_listbox.insert(tk.END, mindful.log_date)

        self.mindfulness_listbox.bind("<<ListboxSelect>>", self.on_select)

        back_button = ttk.Button(self, text="Back to Mindful",
                                 command=lambda: self.controller.show_frame("MindfulScreen"))
        back_button.pack(pady=10)

    def on_select(self, event):
        """
        event for when the user clicks on a ListBox item
        :param event:
        :return:
        """
        selected_index = self.mindfulness_listbox.curselection()
        if selected_index:
            selected_date = self.mindfulness_listbox.get(selected_index)
            mindfulness = get_mindfulness_data(selected_date)
            update_frame = self.controller.get_frame("UpdateMindfulnessScreen")
            update_frame.date_entry.delete(0, tk.END)
            update_frame.date_entry.insert(0, mindfulness.log_date)
            update_frame.date_entry.config(state=tk.DISABLED)
            update_frame.mood_var.set(mindfulness.user_mood)
            update_frame.mood_dropdown.config(state='readonly')
            self.controller.show_frame("UpdateMindfulnessScreen")

    def clear_widgets(self):
        """
        clear the widgets in the frame.
        :return:
        """
        for widget in super().winfo_children():
            widget.destroy()

    def tkraise(self, aboveThis=None):
        """
        override the tkraise function to clear and create widgets to show the new data
        :param aboveThis:
        :return:
        """
        super().tkraise(aboveThis)
        self.clear_widgets()
        self.create_widgets()


class UpdateMindfulnessScreen(ttk.Frame):
    """
    This class describes the Update Mindfulness Screen
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.create_widgets()

    def create_widgets(self):
        """
        Creates the widgets for the screen
        :return:
        """
        ttk.Label(self, text="Date (YYYY-MM-DD)").grid(row=1, column=0, pady=10, padx=10)
        self.date_entry = ttk.Entry(self)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.date_entry.grid(row=1, column=1, pady=10, padx=10)

        ttk.Label(self, text="How is your mood?").grid(row=2, column=0, pady=10, padx=10)
        self.mood_var = tk.StringVar()
        self.mood_dropdown = ttk.Combobox(self, textvariable=self.mood_var)
        self.mood_dropdown['values'] = [e.value for e in Mood]
        self.mood_dropdown.grid(row=2, column=1, pady=10, padx=10)

        submit_button = ttk.Button(self, text="Submit", command=lambda: self.update_mood())
        submit_button.grid(row=3, column=0, pady=10, padx=10)

        back_button = ttk.Button(self, text="Back",
                                 command=lambda: self.controller.show_frame("DisplayMindfulnessScreen"))
        back_button.grid(row=3, column=1, pady=10, padx=10)

    def update_mood(self):
        """
            This function is called when the user clicks the submit button to update the mindfulness data
        :return:
        """
        try:
            update_mindfulness_data(self.mood_var.get(), datetime.strptime(self.date_entry.get(), "%Y-%m-%d").date())
            tkinter.messagebox.showinfo(title="Success", message="Successfully Saved Mood Update")
        except sqlalchemy.exc.SQLAlchemyError:
            tkinter.messagebox.showinfo(title="Error", message="Error updating mood")


class JournalScreen(ttk.Frame):
    """
    This class describes the Journal Screen
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.create_widgets()

    def create_widgets(self):
        """
        This function creates the widgets for the journal screen
        :return:
        """
        ttk.Label(self, text="Title").grid(row=0, column=0, pady=10, padx=10)
        self.title_entry = ttk.Entry(self)
        self.title_entry.grid(row=0, column=1, pady=10, padx=10)

        ttk.Label(self, text="Journal Entry").grid(row=1, column=0, pady=10, padx=10)
        self.journal_entry = tk.Text(self, height=10, width=40)
        self.journal_entry.grid(row=1, column=1, pady=10, padx=10)

        ttk.Label(self, text="Date (YYYY-MM-DD)").grid(row=2, column=0, pady=10, padx=10)
        self.date_entry = ttk.Entry(self, validate='focusout',
                                    validatecommand=(self.register(validate_date_filter), '%P'))
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.date_entry.grid(row=2, column=1, pady=10, padx=10)

        submit_button = ttk.Button(self, text="Submit", command=lambda: self.submit_journal_entry())
        submit_button.grid(row=3, column=0, pady=10, padx=10)

        prev_entries_button = ttk.Button(self, text="Previous Entries",
                                         command=lambda: self.controller.show_frame("DisplayJournalsScreen"))
        prev_entries_button.grid(row=3, column=1, pady=10, padx=10)

        back_button = ttk.Button(self, text="Back to Mindful",
                                 command=lambda: self.controller.show_frame("MindfulScreen"))
        back_button.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

    def submit_journal_entry(self):
        """
        This function is called when the user clicks the submit button
        :return:
        """
        if self.date_entry.get() and self.journal_entry.get("1.0", tk.END):
            try:
                if self.title_entry.get() != '':
                    insert_journal_log(self.title_entry.get(),
                                       self.journal_entry.get("1.0", tk.END),
                                       datetime.strptime(self.date_entry.get(), "%Y-%m-%d").date())
                else:
                    insert_journal_log(datetime.strptime(self.date_entry.get(), "%Y-%m-%d").date(),
                                       self.journal_entry.get("1.0", tk.END),
                                       datetime.strptime(self.date_entry.get(), "%Y-%m-%d").date())

                tkinter.messagebox.showinfo(title="Success", message="Journal Entry Saved Successfully")
            except sqlalchemy.exc.SQLAlchemyError:
                tkinter.messagebox.showinfo(title="Error", message="Journal Entry Failed to Save\n"
                                                                   "To append to an entry created today, click on the "
                                                                   "Previous Entries button")
        if self.date_entry.get() == '':
            messagebox.showinfo(title="Error", message="The Date must not be empty")

    def clear_widgets(self):
        """
        clear the widgets in the frame.
        :return:
        """
        for widget in super().winfo_children():
            widget.destroy()

    def tkraise(self, aboveThis=None):
        """
        override the tkraise function to clear and create widgets to show the new data
        :param aboveThis:
        :return:
        """
        super().tkraise(aboveThis)
        self.clear_widgets()
        self.create_widgets()


class DisplayJournalsScreen(ttk.Frame):
    """
    This class describes the Display Journals Screen
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        """
        This function creates the widgets for the Display Journals Screen
        :return:
        """

        self.instruction_label = ttk.Label(self, text="Click on the date to open the log")
        self.instruction_label.pack(padx=10, pady=10)

        self.journal_listbox = tk.Listbox(self)
        self.journal_listbox.pack(fill="both", expand=True, pady=10, padx=10)

        for journal in get_journal_logs():
            self.journal_listbox.insert(tk.END, journal.journal_date)

        self.journal_listbox.bind("<<ListboxSelect>>", self.on_select)

        self.back_button = ttk.Button(self, text="Back to Journal",
                                      command=lambda: self.controller.show_frame("JournalScreen"))
        self.back_button.pack(pady=10)

    def on_select(self, event):
        """
        When the user makes a selection from the listbox this function is called
        :param event:
        :return:
        """
        selected_index = self.journal_listbox.curselection()
        if selected_index:
            selected_date = self.journal_listbox.get(selected_index)
            journal = get_journal_by_date(selected_date)
            journal_frame = self.controller.get_frame("UpdateJournalScreen")
            journal_frame.date_entry.delete(0, tk.END)
            journal_frame.date_entry.insert(0, journal.journal_date)
            journal_frame.title_entry.delete(0, tk.END)
            journal_frame.title_entry.insert(0, journal.journal_title)
            journal_frame.journal_entry.delete('1.0', tk.END)
            journal_frame.journal_entry.insert('1.0', journal.journal_entry)

            self.controller.show_frame("UpdateJournalScreen")

    def clear_widgets(self):
        """
        This function clears the widgets from the frame
        :return:
        """
        for widget in super().winfo_children():
            widget.destroy()

    def tkraise(self, aboveThis=None):
        """
        override the tkraise function to clear and re-create the widgets to show new data
        :param aboveThis:
        :return:
        """
        super().tkraise(aboveThis)
        self.clear_widgets()
        self.create_widgets()


class UpdateJournalScreen(ttk.Frame):
    """
    This class describes the Update Journal Screen
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.create_widgets()

    def create_widgets(self):
        """
        This function creates the widgets for the Update Journal Screen
        :return:
        """
        ttk.Label(self, text="Title").grid(row=0, column=0, pady=10, padx=10)
        self.title_entry = ttk.Entry(self)
        self.title_entry.grid(row=0, column=1, pady=10, padx=10)

        ttk.Label(self, text="Journal Entry").grid(row=1, column=0, pady=10, padx=10)
        self.journal_entry = tk.Text(self, height=10, width=40)
        self.journal_entry.grid(row=1, column=1, pady=10, padx=10)

        ttk.Label(self, text="Date (YYYY-MM-DD)").grid(row=2, column=0, pady=10, padx=10)
        self.date_entry = ttk.Entry(self, validate='focusout',
                                    validatecommand=(self.register(validate_date_filter), '%P'))
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.date_entry.grid(row=2, column=1, pady=10, padx=10)

        update_button = ttk.Button(self, text="Update", command=lambda: self.update_journal_entry())
        update_button.grid(row=3, column=0, pady=10, padx=10)

        prev_entries_button = ttk.Button(self, text="Previous Entries",
                                         command=lambda: self.controller.show_frame("DisplayJournalsScreen"))
        prev_entries_button.grid(row=3, column=1, pady=10, padx=10)

        back_button = ttk.Button(self, text="Back to Mindful",
                                 command=lambda: self.controller.show_frame("MindfulScreen"))
        back_button.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

    def update_journal_entry(self):
        """
        This function is called when the user clicks the update button to update a journal entry
        :return:
        """
        try:
            update_journal(self.title_entry.get(),
                           self.journal_entry.get("1.0", tk.END),
                           datetime.strptime(self.date_entry.get(), "%Y-%m-%d").date())
            tkinter.messagebox.showinfo(title="Success", message="Update saved successfully")
        except sqlalchemy.exc.SQLAlchemyError:
            tkinter.messagebox.showinfo(title="Error", message="Update Failed")
