"""
    This is the main file of the application. This is the file to be run to run the application
    In the command line, navigate to the directory where this file is housed.
    From the command line run python main.py

"""
# initialize database
from database.database import create_all_tables
from ui import WellnessApp

if __name__ == '__main__':

    #create_all_tables()
    create_all_tables()
    app = WellnessApp()
    app.mainloop()