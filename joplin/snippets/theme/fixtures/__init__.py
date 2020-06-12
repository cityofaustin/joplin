from .test_cases.kitchen_sink import kitchen_sink
from .test_cases import janis_themes


# You can import any test_case fixture individually
# Or you can load them all with this function
def load_all():
    kitchen_sink()
    janis_themes.pets()
    janis_themes.government_business()
    janis_themes.jobs()
    janis_themes.housing_utilities()
    janis_themes.health_safety()
    janis_themes.explore_visit()
    janis_themes.permits_tickets()
