"""
    This script contains the functions related to finance data persistence.

"""
from sqlalchemy.orm import Session

from database.database import DBConnection, Finance


def insert_finance_data(income, grocery, utility, rent, food, misc, date):
    """
    This function is used for inserting data into the finance table
    """
    conn = DBConnection()
    engine = conn.get_sqlalchemy_engine()

    with Session(engine) as session:
        firstEntry = Finance(
            income=income,
            grocery_expense=grocery,
            utility_expense=utility,
            rent=rent,
            food_expense=food,
            misc_expense=misc,
            log_date=date
        )
        session.add(firstEntry)
        session.commit()


def get_all_finance_data():
    """
    This function is used for getting all the finance data
    """
    conn = DBConnection()
    engine = conn.get_sqlalchemy_engine()
    session = Session(engine)
    financeList = []
    for finance in session.query(Finance):
        financeList.append(finance)

    return financeList


def get_all_finance_data_between_dates(date1, date2):
    """
        This function returns all the finance data between two dates
    """
    conn = DBConnection()
    engine = conn.get_sqlalchemy_engine()
    session = Session(engine)

    financeList = []
    for finance in session.query(Finance).filter(Finance.log_date.between(date1, date2)):
        financeList.append(finance)

    return financeList


def get_finance_log_by_date(date):
    """
    This function gets the finance log by date
    :param date:
    :return:
    """
    conn = DBConnection()
    engine = conn.get_sqlalchemy_engine()
    session = Session(engine)
    return session.query(Finance).filter(Finance.log_date == date).first()


def update_finance_log(income, grocery, utility, rent, food, misc, date):
    """
        This function updates a finance log
    """
    conn = DBConnection()
    engine = conn.get_sqlalchemy_engine()
    session = Session(engine)
    session.query(Finance).filter(Finance.log_date == date).update({
        'income': income,
        'grocery_expense': grocery,
        'utility_expense': utility,
        'rent': rent,
        'food_expense': food,
        'misc_expense': misc
    })
    session.commit()


def delete_finance_log(date):
    """
        This function deletes a finance log
    """
    conn = DBConnection()
    engine = conn.get_sqlalchemy_engine()
    session = Session(engine)
    session.query(Finance).filter(Finance.log_date == date).delete()
    session.commit()
