from wagtail.core import blocks
from wagtail.snippets.blocks import SnippetChooserBlock


class SnippetChooserBlockWithAPIGoodness(SnippetChooserBlock):
    def get_api_representation(self, model_instance, context=None):
        return model_instance.serializable_data()


class WhatDoIDoWithBlock(blocks.StaticBlock):
    class Meta:
        icon = 'bin'
        label = 'What do I do with...'
        admin_text = label


class CollectionScheduleBlock(blocks.StaticBlock):
    class Meta:
        icon = 'bin'
        label = 'Collection Schedule'
        admin_text = label


class RecollectBlock(blocks.StaticBlock):
    class Meta:
        icon = 'bin'
        label = 'Recollect'
        admin_text = label


class DayChoiceBlock(blocks.ChoiceBlock):
    choices = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]


"""
these were implemented but NOT used anywhere
we totally could use them, or consider them an example of how to design a reuseable component
using StreamField stuff
"""


class AMChoiceBlock(blocks.ChoiceBlock):
    choices = [
        ('am', 'A.M.'),
        ('pm', 'P.M'),
    ]


class RecurrenceChoiceBlock(blocks.ChoiceBlock):
    choices = [
        ('1', '1st'),
        ('2', '2nd'),
        ('3', '3rd'),
        ('4', '4th')
    ]


class OperatingHoursExceptionsBlock(blocks.StructBlock):
    open_or_closed = blocks.ChoiceBlock(choices=[('open', 'Open'), ('closed', 'Closed')])
    recurrence = RecurrenceChoiceBlock()
    start_time = blocks.TimeBlock()
    start_time_AM = AMChoiceBlock()
    end_time = blocks.TimeBlock()
    end_time_AM = AMChoiceBlock()


class OperatingHoursBlock(blocks.StructBlock):
    open = blocks.BooleanBlock()
    start_time = blocks.TimeBlock()
    end_time = blocks.TimeBlock()

    class Meta:
        icon = 'user'


class HoursByDay(blocks.StructBlock):
    monday = blocks.ListBlock(OperatingHoursBlock())
    tuesday = blocks.ListBlock(OperatingHoursBlock())
    wednesday = blocks.ListBlock(OperatingHoursBlock())
    thursday = blocks.ListBlock(OperatingHoursBlock())
    friday = blocks.ListBlock(OperatingHoursBlock())
    saturday = blocks.ListBlock(OperatingHoursBlock())
    sunday = blocks.ListBlock(OperatingHoursBlock())
