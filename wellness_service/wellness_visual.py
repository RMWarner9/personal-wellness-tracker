"""
This script file contains the functions for setting up a pie chart to be used for displaying wellness data
"""
from wellness_service.financial_wellness import calculate_financial_breakdown, calculate_financial_breakdown_by_date
from wellness_service.mindfulness import calculate_mood_breakdown, \
    calculate_mood_breakdown_by_date


def show_financial_wellness_pie_chart(figure):
    """
    This function accepts a figure to add the subplot to and gets the pie chart ready to be displayed.
    This returns all existing financial wellness data the user has entered
    :param figure:
    :return:
    """
    finance_dictionary = calculate_financial_breakdown()
    labels = []
    data = []
    # add a subplot to the figure (1x1 grid, first subplot)
    plt = figure.add_subplot(1, 1, 1)
    for finance in finance_dictionary:
        if finance == 'total_debt':
            labels.append(f"{finance}: {finance_dictionary[finance]}")
            data.append(100)
            break
        if finance != 'total_income' and finance != 'total_expense':
            if finance_dictionary[finance] != 0:
                labels.append(finance)
                data.append(finance_dictionary[finance])

    plt.pie(data, labels=labels)
    plt.legend(title="Expenses", bbox_to_anchor=(0.90, 0.5))
    plt.set_title("Financial Wellness")
    # tight_layout() adjusts the subplots parameters to fit properly
    figure.tight_layout()


def show_financial_wellness_by_date(figure, date1, date2):
    """
        This function accepts a figure to add the subplot to and gets the pie chart ready to be displayed
        This returns the financial wellness data between the two dates provided
        :param date2:
        :param date1:
        :param figure:
        :return:
        """
    finance_dictionary = calculate_financial_breakdown_by_date(date1, date2)
    labels = []
    data = []
    # add a subplot to the figure (1x1 grid, first subplot)
    plt = figure.add_subplot(1, 1, 1)
    for finance in finance_dictionary:
        if finance != 'total_income' and finance != 'total_expense':
            if finance_dictionary[finance] != 0:
                labels.append(finance)
                data.append(finance_dictionary[finance])

    plt.pie(data, labels=labels)
    plt.legend(title="Expenses", bbox_to_anchor=(0.90, 0.5))
    plt.set_title("Financial Wellness")
    # tight_layout() adjusts the subplots parameters to fit properly
    figure.tight_layout()


def show_mood_wellness_pie_chart(figure):
    """
    This function accepts a figure to add the subplot to. This function returns a pie chart containing
    all mood data the user has entered
    :param figure:
    :return:
    """
    mood_dictionary = calculate_mood_breakdown()
    labels = []
    data = []
    # add a subplot to the figure (1x1 grid, first subplot)
    plt = figure.add_subplot(1, 1, 1)
    for item in mood_dictionary:
        if item != 'total_moods_logged':
            if mood_dictionary[item] == 0:
                continue
            else:
                labels.append(item)
                data.append(mood_dictionary[item])
    plt.pie(data, labels=labels)
    plt.legend(title="Moods", bbox_to_anchor=(0.90, 0.5))
    plt.set_title("Mood Wellness")
    # tight_layout() adjusts the subplots parameters to fit properly
    figure.tight_layout()


def show_mood_wellness_pie_chart_date_filter(figure, date1, date2):
    """
    This function prepares the pie chart containing all of the mood data between two selected dates
    :param figure:
    :param date1:
    :param date2:
    :return:
    """
    mood_dictionary = calculate_mood_breakdown_by_date(date1, date2)
    labels = []
    data = []
    # add a subplot to the figure (1x1 grid, first subplot)
    plt = figure.add_subplot(1, 1, 1)
    for item in mood_dictionary:
        if item != 'total_moods_logged':
            if mood_dictionary[item] == 0:
                continue
            else:
                labels.append(item)
                data.append(mood_dictionary[item])
    plt.pie(data, labels=labels)
    plt.legend(title="Moods", bbox_to_anchor=(0.90, 0.5))
    plt.set_title("Mood Wellness")
    # tight_layout() adjusts the subplots parameters to fit properly
    figure.tight_layout()
