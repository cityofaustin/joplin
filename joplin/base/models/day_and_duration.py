from django.db import models

from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel


class DayAndDuration(ClusterableModel):
    """
    creates a model to choose day of week and hourly ranges
    you can use this to define operating hours for a service or location
    """
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    SUNDAY = 'Sunday'
    DAY_OF_WEEK_CHOICES = (
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    )

    day_of_week = models.CharField(max_length=20, choices=DAY_OF_WEEK_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    panels = [


        FieldRowPanel(
            children=[
                FieldPanel('day_of_week', classname="col5"),
                FieldPanel('start_time', classname="col3"),
                FieldPanel('end_time', classname="col3"),

            ],
            classname="full"
        ),



    ]

    def __str__(self):
        return f'{self.day_of_week} {self.start_time} - {self.end_time}'
