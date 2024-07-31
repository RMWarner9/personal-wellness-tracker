"""
 This script contains the functions related to journal data persistence
"""
from sqlalchemy.orm import Session

from database.database import DBConnection, Journal


def insert_journal_data(title, entry, date):
    """
        This function is used for inserting data into the journal table
    """
    conn = DBConnection()
    engine = conn.get_sqlalchemy_engine()

    with Session(engine) as session:
        firstEntry = Journal(
            journal_title=title,
            journal_entry=entry,
            journal_date=date
        )
        session.add(firstEntry)
        session.commit()


def get_all_journal_data():
    """
        This function returns all the journal data stored
    """
    conn = DBConnection()
    engine = conn.get_sqlalchemy_engine()
    session = Session(engine)
    journalList = []
    for journal in session.query(Journal):
        journalList.append(journal)

    return journalList


def get_all_journal_data_between_dates(date1, date2):
    """
        This function returns all the journal data between two dates
    """
    conn = DBConnection()
    engine = conn.get_sqlalchemy_engine()
    session = Session(engine)
    journalList = []
    for journal in session.query(Journal).filter(Journal.journal_date.between(date1, date2)):
        journalList.append(journal)
    return journalList


def get_journal_log_by_date(date):
    """
    This function returns the journal log by date
    :param date:
    :return:
    """
    conn = DBConnection()
    engine = conn.get_sqlalchemy_engine()
    session = Session(engine)
    return session.query(Journal).filter(Journal.journal_date == date).first()


def update_journal_log(title, entry, date):
    """
        This function updates a journal log
    """
    conn = DBConnection()
    engine = conn.get_sqlalchemy_engine()
    session = Session(engine)
    session.query(Journal).filter(Journal.journal_date == date).update({
        'journal_title': title,
        'journal_entry': entry
    })
    session.commit()
    for journal in session.query(Journal):
        print(journal)


def delete_journal_log(date):
    """
        This function deletes a journal log
    """
    conn = DBConnection()
    engine = conn.get_sqlalchemy_engine()
    session = Session(engine)
    session.query(Journal).filter(Journal.journal_date == date).delete()
    session.commit()
