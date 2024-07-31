"""
This script file handles the retrieval and processing in finance data
"""
from database.finance_data_persistence import get_all_finance_data, get_all_finance_data_between_dates, \
    insert_finance_data, update_finance_log, delete_finance_log, get_finance_log_by_date


def calculate_financial_breakdown():
    """
    This function returns a dictionary containing all financial logs
    """
    # Get the data
    finance = get_all_finance_data()
    return get_finance_breakdown_dictionary(finance)


def calculate_financial_breakdown_by_date(date1, date2):
    """
    This function returns a dictionary containing all financial logs between two dates
    :param date1:
    :param date2:
    :return:
    """
    finance = get_all_finance_data_between_dates(date1, date2)
    return get_finance_breakdown_dictionary(finance)


def get_finance_breakdown_dictionary(finances):
    """
    This function creates the financial breakdown dictionary
    :param finances:
    :return:
    """
    total_income = 0
    total_grocery = 0
    total_utility = 0
    total_rent = 0
    total_food = 0
    total_misc = 0
    # In order to display the data in the pie chart, the data must sum up to 100.
    if len(finances) != 0:

        for finance in finances:
            total_income += finance.income
            total_grocery += finance.grocery_expense
            total_utility += finance.utility_expense
            total_rent += finance.rent
            total_food += finance.food_expense
            total_misc += finance.misc_expense

        total_expense = total_grocery + total_utility + total_rent + total_food + total_misc
        # if the user has over spent, return a dictionary containing the amount over spent
        if total_expense > total_income:
            return {
                'total_debt': total_income - total_expense
            }
        else:
            financial_breakdown_dictionary = {'total_income': total_income,
                                              'total_grocery': ((total_grocery / total_income) * 100),
                                              'total_utility': ((total_utility / total_income) * 100),
                                              'total_rent': ((total_rent / total_income) * 100),
                                              'total_food': ((total_food / total_income) * 100),
                                              'total_misc': ((total_misc / total_income) * 100),
                                              'total_unspent': (((total_income - total_expense) / total_income) * 100),
                                              'total_expense': total_expense}
            return financial_breakdown_dictionary
    else:
        return {
            'no_entries': 100
        }


def insert_financial_wellness_data(income, grocery, utility, rent, food, misc, date):
    """
    Insert financial data
    :param income:
    :param grocery:
    :param utility:
    :param rent:
    :param food:
    :param misc:
    :param date:
    :return:
    """
    insert_finance_data(income, grocery, utility, rent, food, misc, date)


def update_financial_wellness_data(income, grocery, utility, rent, food, misc, date):
    """
    Update Financial Data
    :param income:
    :param grocery:
    :param utility:
    :param rent:
    :param food:
    :param misc:
    :param date:
    :return:
    """
    update_finance_log(income, grocery, utility, rent, food, misc, date)


def delete_financial_wellness_data(date):
    """
    Delete financial data
    :param date:
    :return:
    """
    delete_finance_log(date)


def get_financial_wellness_data(date):
    """
    Get financial wellness data by date
    :param date:
    :return:
    """
    return get_finance_log_by_date(date)


def get_all_financial_wellness_data():
    """
    Returns all finance data
    :return:
    """
    return get_all_finance_data()
