
'''
    components.py contains elements that may be used
    interchangeably with multiple fixtures
'''
from pages.home_page.models import HomePage


def home():
    return HomePage.objects.first()


def location_hours():
    return {
        "monday_start_time": "02:00:00",
        "monday_end_time": "05:00:00",
        "monday_start_time_2": "06:00:00",
        "monday_end_time_2": "16:00:00",
        "tuesday_start_time": "02:00:00",
        "tuesday_end_time": "05:00:00",
        "tuesday_start_time_2": "06:00:00",
        "tuesday_end_time_2": "16:00:00",
        "wednesday_start_time": "02:00:00",
        "wednesday_end_time": "05:00:00",
        "wednesday_start_time_2": "06:00:00",
        "wednesday_end_time_2": "16:00:00",
        "thursday_start_time": "02:00:00",
        "thursday_end_time": "05:00:00",
        "thursday_start_time_2": "06:00:00",
        "thursday_end_time_2": "16:00:00",
        "friday_start_time": "02:00:00",
        "friday_end_time": "05:00:00",
        "friday_start_time_2": "06:00:00",
        "friday_end_time_2": "16:00:00",
        "saturday_start_time": "02:00:00",
        "saturday_end_time": "05:00:00",
        "saturday_start_time_2": "06:00:00",
        "saturday_end_time_2": "16:00:00",
        "sunday_start_time": "02:00:00",
        "sunday_end_time": "05:00:00",
        "sunday_start_time_2": "06:00:00",
        "sunday_end_time_2": "16:00:00",
    }
