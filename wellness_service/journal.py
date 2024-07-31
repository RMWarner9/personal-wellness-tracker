"""
This script file handles the functions for interacting with the journal
"""
from database.journal_data_persistence import insert_journal_data, get_all_journal_data, get_journal_log_by_date, \
    get_all_journal_data_between_dates, update_journal_log, delete_journal_log


def insert_journal_log(title, entry, date):
    """
    insert a journal into the database
    :param title:
    :param entry:
    :param date:
    :return:
    """
    insert_journal_data(title, entry, date)


def get_journal_logs():
    """
    get all journal logs
    :return:
    """
    return get_all_journal_data()


def get_journal_by_date(date):
    """
    Get the journal log by date
    :param date:
    :return:
    """
    return get_journal_log_by_date(date)


def get_journals_between_dates(date1, date2):
    """
    get journals between dates
    :param date1:
    :param date2:
    :return:
    """
    return get_all_journal_data_between_dates(date1, date2)


def update_journal(title, entry, date):
    """
    update journal
    :param title:
    :param entry:
    :param date:
    :return:
    """
    update_journal_log(title, entry, date)


def delete_journal(date):
    """
    delete journal
    :param date:
    :return:
    """
    delete_journal_log(date)
