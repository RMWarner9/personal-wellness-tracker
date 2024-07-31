"""
This script file handles the interactions for getting and processing the mindfulness data
"""
from database.mindfulness_data_persistence import get_all_mindfulness_data, get_all_mindfulness_data_between_dates, \
    get_mindfulness_log_by_date, insert_mindfulness_data, update_mindfulness_log, delete_mindfulness_log


def get_mindfulness_breakdown_dictionary(mindfulness):
    """
    This function provides a dictionary containing the label and data values to be used by the pie chart
    :param mindfulness:
    :return:
    """
    total_moods_logged = 0
    total_happy = 0
    total_sad = 0
    total_frustrated = 0
    total_content = 0
    total_stressed = 0
    total_grateful = 0
    if len(mindfulness) != 0:
        for mindful in mindfulness:
            total_moods_logged += 1
            if mindful.user_mood.upper() == 'HAPPY':
                total_happy += 1
            elif mindful.user_mood.upper() == 'SAD':
                total_sad += 1
            elif mindful.user_mood.upper() == 'FRUSTRATED':
                total_frustrated += 1
            elif mindful.user_mood.upper() == 'CONTENT':
                total_content += 1
            elif mindful.user_mood.upper() == 'STRESSED':
                total_stressed += 1
            elif mindful.user_mood.upper() == 'GRATEFUL':
                total_grateful += 1
            else:
                continue

        mood_breakdown_dictionary = {
            'total_moods_logged': total_moods_logged,
            'happy': (total_happy / total_moods_logged) * 100,
            'sad': (total_sad / total_moods_logged) * 100,
            'frustrated': (total_frustrated / total_moods_logged) * 100,
            'content': (total_content / total_moods_logged) * 100,
            'stressed': (total_stressed / total_moods_logged) * 100,
            'grateful': (total_grateful / total_moods_logged) * 100
        }

        return mood_breakdown_dictionary
    else:
        return {
            'no_moods_logged': 100
        }


def get_mindfulness_data_history():
    """
    returns all mindfulness data
    :return:
    """
    return get_all_mindfulness_data()


def calculate_mood_breakdown():
    """
        returns a dictionary containing the mindfulness label and data for the pie chart
    :return:
    """
    mindfulness = get_all_mindfulness_data()
    return get_mindfulness_breakdown_dictionary(mindfulness)


def calculate_mood_breakdown_by_date(date1, date2):
    """
    returns a dictionary containing the mindfulness label and data for the pie chart between two dates
    :param date1:
    :param date2:
    :return:
    """
    mindfulness = get_all_mindfulness_data_between_dates(date1, date2)
    return get_mindfulness_breakdown_dictionary(mindfulness)


def get_mindfulness_data(date):
    """
    gets the mindfulness data by date
    :param date:
    :return:
    """
    return get_mindfulness_log_by_date(date)


def insert_mindfulness_log(mood, date):
    """
    insert the mindfulness data
    :param mood:
    :param date:
    :return:
    """
    insert_mindfulness_data(mood, date)


def update_mindfulness_data(mood, date):
    """
    Update the mindfulness data
    :param mood:
    :param date:
    :return:
    """
    update_mindfulness_log(mood, date)


def delete_mindfulness_data(date):
    """
    Delete mindfulness data
    :param date:
    :return:
    """
    delete_mindfulness_log(date)
