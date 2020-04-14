'''
    components.py contains elements that may be used
    interchangeably with multiple fixtures
'''
from pages.home_page.models import HomePage
import os


def home():
    return HomePage.objects.first()


dynamic_content = '<h2>Bulk item pickup do’s and don’ts</h2><p>Do not put bulk items in bags, boxes, or other containers. Bags will be treated as extra trash and are subject to extra trash fees.</p><p>Do not place any items under low hanging tree limbs or power lines.</p><p>Do not place items in an alley in any area in front of a vacant lot or in front of a business. Items will not be collected from these areas.</p><p>To prevent damage to your property, keep bulk items 5 feet away from your:</p><ul><li>Trash cart</li><li>Mailbox</li><li>Fences or walls</li><li>Water meter</li><li>Telephone connection box</li><li>Parked cars</li></ul>'

dynamic_content_list = [
    {'type': 'collection_schedule_block', 'value': None, 'id': '4c02f0f9-5e7a-4ddb-b1b7-c6b3f1da159d'},
    {'type': 'recollect_block', 'value': None, 'id': '826f0f09-ed6e-4d81-a9eb-cfceef23c82a'}
]

steps_with_appblocks = [
    {
        'type': 'basic_step',
        'value': '<p>Use the this tool to see what bulk items can be picked '
                 'up. Bulk items are items that are too large for your trash '
                 'cart, such as appliances, furniture, and '
                 'carpet.</p><p></p><p><code>APPBLOCK: What do I do '
                 'with</code></p>'
    },
    {
        'type': 'basic_step',
        'value': '<p>Consider donating your items before placing them on the '
                 'curb for pickup.</p>'
    },
    {
        'type': 'basic_step',
        'value': '<p>Look up your bulk pickup weeks. We only collect bulk '
                 'items from Austin residential trash and recycling customers '
                 'twice a year, and customers have different pickup '
                 'weeks.</p><p></p><p><code>APPBLOCK: Collection '
                 'Schedule</code></p>'
    },
    {
        'type': 'basic_step',
        'value': '<p>Review the bulk item pickup do’s and don’ts below.</p>'
    },
    {
        'type': 'basic_step',
        'value': '<p>Place bulk items at the curb in front of your house by '
                 '6:30 am on the first day of your scheduled collection '
                 'week.</p>'
    },
    {
        'type': 'basic_step',
        'value': '<p>Separate items into three '
                 'piles:</p><ul><li>Metal—includes appliances, doors must be '
                 'removed</li><li>Passenger car tires—limit of eight tires per '
                 'household, rims must be removed, no truck or tractor '
                 'tires</li><li>Non-metal items—includes carpeting and '
                 'nail-free lumber</li></ul>'
    },
    {
        'type': 'basic_step',
        'value': '<p>The three separate piles are collected by different '
                 'trucks and may be collected at different times throughout '
                 'the week.</p>'
    }
]

steps_2 = [
    {
        'type': 'basic_step',
        'value': '<p>Separate items into three '
                 'piles:</p><ul><li>Metal—includes appliances, doors must be '
                 'removed</li><li>Passenger car tires—limit of eight tires per '
                 'household, rims must be removed, no truck or tractor '
                 'tires</li><li>Non-metal items—includes carpeting and '
                 'nail-free lumber</li></ul>'
    },
    {
        'type': 'basic_step',
        'value': '<p>The three separate piles are collected by different '
                 'trucks and may be collected at different times throughout '
                 'the week.</p>'
    }
]

step_with_options = [
    {
        "type": "step_with_options_accordian",
        "value": {
            "options": [
                {
                    "option_description": "<p>Required information</p><ul><li>What happened</li></ul><p>Optional information</p><ul><li>Date and time</li><li>Officer(s) involved</li></ul><p></p><p><a href=\"https://forms.austin.gov/police-thank/what-happened\">Start</a></p>",
                    "option_name": "Online"
                },
                {
                    "option_description": "<p>Call the Office of Police Oversight at (512) 972-2676. We’d be happy to speak with you.</p><p>If you need an interpreter, you can call with a friend to interpret for you or ask for an interpreter. Just tell us the language you prefer.</p><p>Office hours are Monday through Friday, 8 am to 5 pm.</p>",
                    "option_name": "Over the phone"
                },
                {
                    "option_description": "<p>You can share thanks in person at the <a href=\"https://janis.austintexas.io/en/location/office-of-police-oversight\">Office of Police Oversight</a> at 1520 Rutherford Lane, Austin, TX 78754. We are in Building 1, on the 2nd floor, Suite 211. Visitor parking is in front of the main entrance.</p><p>Office hours are Monday through Friday, 8 am to 5 pm.</p>",
                    "option_name": "In person"
                },
                {
                    "option_description": "<p><a href=\"https://forms.austin.gov/files/OPO_thanks-form_print_English.pdf\">Download the thanks form (PDF)</a>. Print and fill out the form, then mail it to:</p><p>Office of Police Oversight</p><p>P.O. Box 1088</p><p>Austin, TX 78767</p>",
                    "option_name": "By mail"
                }
            ],
            "options_description": "<p>Select an option for saying thanks.</p>"
        }
    },
]
