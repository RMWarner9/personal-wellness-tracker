# Personal Wellness Tracker

## Introduction
The Personal Wellness Tracker will be an application that allows users to track and visualize their wellness in different aspects. The application will focus on visualizing financial and emotional well-being to aid the user in making better financial and emotional decisions.
This software's intended audience or users would be anyone interested in having an application that visualizes their financial and emotional wellness while being interested in data privacy as analysis, and storage are done locally. 

### Demo:
https://www.youtube.com/watch?v=zfDTaYSgnR4
## Requirements Analysis
### Necessary Libraries:
•	Tkinter 
•	Matplotlib
•	SqlAlchemy
•	Sqlite

### Requirements:
•	The Personal Wellness Tracker shall allow the user to:
  o	Track financial wellness through:
    -	Displaying the user’s financial analysis:
      •	Spending vs income
      •	Allow the user to select a date range to view
      •	A pie chart providing a visual of the users' expenses
    -	Allowing the user to:
      •	Input salary and expenses
  o	Track emotional wellness:
    -	Displaying the user’s wellness analysis:
      •	Display the user’s mood history via week or month.
      •	Allow the user to select which month or week for emotional analysis
  o	Journal:
    -	Allow the user to:
      •	Create, read, update, and delete journal entries
## Module/Component Design:
  ### Structure
  The following are the main components of the application
  Main.py
    •	Serves as the entry point to the program
  Ui.py
    •	UI.py may control two different UI displays.
      o	The UI may consist of an interactive CLI or GUI via Tkinter.
    •	Contains the UI definitions for tkinter interactions with wellness.py
    •	Contains logic for displaying pie graphs for wellness information.
  Wellness-service.py
    •	Serves as the middle-man between all of the wellness services
    •	The wellness-service module will be responsible for data validation before interacting with other wellness modules as well as for calling other modules when needed.
  Finance.py
    •	The finance.py module serves as a module that fetches financial data from the database for displaying to the user
    •	A module fetching financial data from the database for displaying to the user and analysis.
    •	The finance.py module will allow users to:
      o	Create, read, update, and delete financial data
  Mindfulness.py
    •	The mindfulness.py module is a module that fetches historical mood data from the database to display to the user. 
    •	The mindfulness.py module will allow users to:
      o	Create, read, and update mood data
  Journal.py
    •	The journal.py module is a module that will allow a user to retrieve historical journal data.
    •	The journal.py module will allow users to:
      o	Create, read, update, and delete journal entries
  Database.py
    •	The database.py module will handle the database logic for retrieving data, checking if the in-memory database exists, and creating the database. 
    •	The database.py module will use SQLAlchemy as an Object Relational Mapper to assist with database interactions.
