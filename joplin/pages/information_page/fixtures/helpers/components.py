'''
    components.py contains elements that may be used
    interchangeably with multiple fixtures
'''
from pages.home_page.models import HomePage
import os


def home():
    return HomePage.objects.first()
