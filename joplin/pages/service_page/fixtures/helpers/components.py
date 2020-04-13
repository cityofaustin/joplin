'''
    components.py contains elements that may be used
    interchangeably with multiple fixtures
'''
from pages.home_page.models import HomePage
import os


def home():
    return HomePage.objects.first()


dynamic_content = '<h2>Bulk item pickup do’s and don’ts</h2><p>Do not put bulk items in bags, boxes, or other containers. Bags will be treated as extra trash and are subject to extra trash fees.</p><p>Do not place any items under low hanging tree limbs or power lines.</p><p>Do not place items in an alley in any area in front of a vacant lot or in front of a business. Items will not be collected from these areas.</p><p>To prevent damage to your property, keep bulk items 5 feet away from your:</p><ul><li>Trash cart</li><li>Mailbox</li><li>Fences or walls</li><li>Water meter</li><li>Telephone connection box</li><li>Parked cars</li></ul>'

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
