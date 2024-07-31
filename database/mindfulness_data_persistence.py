"""
    This script file contains the functions related to mindfulness data persistence
"""
from sqlalchemy.orm import Session

from database.database import DBConnection, Mindfulness


def insert_mindfulness_data(user_mood, log_date):
    """
    This function is used for inserting data into the mindfulness table
    """
    conn = DBConnection()
    engine = conn.get_sqlalchemy_engine()

    with Session(engine) as session:
        firstEntry = Mindfulness(
            user_mood=user_mood,
            log_date=log_date
        )

        session.add(firstEntry)
        session.commit()


def get_all_mindfulness_data():
    """
        This function is used for getting all mindfulness data
    """
    conn = DBConnection()
    engine = conn.get_sqlalchemy_engine()
    session = Session(engine)
    mindfulnessList = []
    for mindfulness in session.query(Mindfulness):
        mindfulnessList.append(mindfulness)

    return mindfulnessList


def get_all_mindfulness_data_between_dates(date1, date2):
    """
        This function returns all mindfulness data between two dates
    """
    conn = DBConnection()
    engine = conn.get_sqlalchemy_engine()
    session = Session(engine)

    mindfulnessList = []
    for mindfulness in session.query(Mindfulness).filter(Mindfulness.log_date.between(date1, date2)):
        mindfulnessList.append(mindfulness)

    return mindfulnessList


def get_mindfulness_log_by_date(date):
    """
        This function gets the mindfulness log by date
    :param date:
    :return:
    """
    conn = DBConnection()
    engine = conn.get_sqlalchemy_engine()
    session = Session(engine)
    return session.query(Mindfulness).filter(Mindfulness.log_date == date).first()


def update_mindfulness_log(mood, log_date):
    """
        This function updates the mindfulness log
    """
    conn = DBConnection()
    engine = conn.get_sqlalchemy_engine()
    session = Session(engine)
    session.query(Mindfulness).filter(Mindfulness.log_date == log_date).update({'user_mood': mood})
    session.commit()


def delete_mindfulness_log(date):
    """
        This function deletes the mindfulness log
    """
    conn = DBConnection()
    engine = conn.get_sqlalchemy_engine()
    session = Session(engine)
    session.query(Mindfulness).filter(Mindfulness.log_date == date).delete()
    session.commit()
