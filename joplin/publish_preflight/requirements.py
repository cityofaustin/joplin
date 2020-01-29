from django.core.exceptions import ValidationError

# Check if field value is not empty
# Default criteria for FieldPublishRequirement
def is_not_empty(field_value):
    if isinstance(field_value, str):
        return not (not field_value.strip())
    else:
        return not (not field_value)

# Check if relation has at least one entry
# Default criteria for RelationPublishRequirement
def has_at_least_one(relation_value):
    return (len(relation_value) > 1)

placeholder_message = "Publish Requirement not met"

# A Publish Requirement for a simple field
class FieldPublishRequirement():
    def __init__(self, field_name, criteria=is_not_empty, message=placeholder_message, langs=None):
        self.field_name = field_name
        self.criteria = criteria
        self.message = ValidationError(message)
        self.langs = langs

    def evaluate(self, field_name, field_value):
        result = self.criteria(field_value)
        return {
            "result": result,
            "field_name": field_name,
            "message": self.message
        }

    def check_criteria(self, data):
        field_name = self.field_name
        # If field is not translated, then get check value of "field_name"
        # If field is translated, then check value of each applicable language
        if self.langs:
            for lang in self.langs:
                translated_field_name = f'{self.field_name}_{lang}'
                if translated_field_name in data:
                    field_value = data.get(translated_field_name)
                    return self.evaluate(translated_field_name, field_value)
                else:
                    raise ValidationError(f"Field required for publish '{translated_field_name}' does not exist.")
        else:
            field_value = data.get(field_name)
            return self.evaluate(field_name, field_value)


# A Publish Requirement for a related ClusterableModel
class RelationPublishRequirement():
    def __init__(self, field_name, criteria=has_at_least_one, message=placeholder_message):
        self.field_name = field_name
        self.criteria = criteria
        self.message = message

    def evaluate(self, field_name, data):
        result = self.criteria(data)
        return {
            "result": result,
            "field_name": field_name,
            "message": self.message
        }

    def check_criteria(self, form):
        formsets = form.formsets
        field_name = self.field_name
        if field_name in formsets:
            data = formsets.get(field_name).cleaned_data
            return self.evaluate(field_name, data)
        else:
            raise ValidationError(f"Field required for publish '{field_name}' does not exist.")

class ConditionalPublishRequirement():
    def __init__(self, requirement1, operation, requirement2, message=placeholder_message):
        self.requirement1 = requirement1
        self.operation = operation
        self.requirement2 = requirement2
        self.message = message

    operation_map = {
        "or": lambda a,b: a or b,
        "and": lambda a,b: a and b,
    }

    # TODO: finish
    def check_criteria(self, value):
        op_func = self.operation_map[self.operation]
        return op_func(
            self.requirement1.check_criteria(value),
            self.requirement2.check_criteria(value),
        )

# sample
publish_requirements = (
    FieldPublishRequirement("description", langs=["en"]),
    FieldPublishRequirement("additional_content", langs=["en"]),
    ConditionalPublishRequirement(
        RelationPublishRequirement("topic"),
        "or",
        ConditionalPublishRequirement(
            RelationPublishRequirement("related_department"),
            "or",
            FieldPublishRequirement("coa_global"),
        ),
        "You must have at least 1 topic or 1 department or 'Top Level' checked."
    ),
)
