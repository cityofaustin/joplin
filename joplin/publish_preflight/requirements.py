from django.core.exceptions import ValidationError


# Check if field value is not empty
# Default criteria for FieldPublishRequirement
def is_not_empty(field_value):
    if isinstance(field_value, str):
        return not (not field_value.strip())
    else:
        return not (not field_value)


# Check if relation has at least one entry
# And that there is at least 1 entry that is not set for deletion.
# Default criteria for RelationPublishRequirement
def has_at_least_one(relation_value):
    # relation_value could be a list with an empty dictionary
    if len(relation_value) > 0 and bool(relation_value[0]):
        return any(not i["DELETE"] for i in relation_value)
    else:
        return False


def streamfield_has_length(stream_value):
    if not stream_value:
        return False
    return len(stream_value) > 0

placeholder_message = "Publish Requirement not met"

# A ValidationError with an additional "publish_error_data" attribute
# The "publish_error_data" attribute is passed to the frontend edit/ page
# And used to add custom publishing error messages on fields.
class PublishRequirementError(ValidationError):
    def __init__(self, *args, **kwargs):
        self.publish_error_data = kwargs.pop("publish_error_data", None)
        super(PublishRequirementError, self).__init__(*args, **kwargs)


def publish_error_factory(field_name, field_type, message):
    return {
        "passed": False,
        "publish_requirement_errors": [PublishRequirementError(message, publish_error_data={
            "field_name": field_name,
            "message": message,
            "field_type": field_type,
        })]
    }


def publish_success_factory():
    return {
        "passed": True,
    }


class BasePublishRequirement:
    # evaluate() is used by FieldPublishRequirement, StreamfieldPublishRequirement, and RelationPublishRequirement
    # All PublishRequirements must return data in the same structure: either a publish_error_factory instance or
    # a publish_success_factory instance
    def evaluate(self, field_name, field_value):
        result = self.criteria(field_value)
        if not result:
            return publish_error_factory(
                field_name,
                self.field_type,
                self.message,
            )
        else:
            return publish_success_factory()


# A Publish Requirement for a simple field
class FieldPublishRequirement(BasePublishRequirement):
    def __init__(self, field_name, criteria=is_not_empty, message=placeholder_message, langs=None):
        self.field_type = "field"
        self.field_name = field_name
        self.criteria = criteria
        self.message = message
        self.langs = langs

    def check_criteria(self, form):
        field_name = self.field_name
        data = form.cleaned_data
        # If field is not translated, then get check value of "field_name"
        # If field is translated, then check value of each applicable language
        if self.langs:
            for lang in self.langs:
                translated_field_name = f'{self.field_name}_{lang}'
                if translated_field_name in data:
                    field_value = data.get(translated_field_name)
                    return self.evaluate(translated_field_name, field_value)
                else:
                    raise KeyError(f"Field required for publish '{translated_field_name}' does not exist.")
        else:
            field_value = data.get(field_name)
            return self.evaluate(field_name, field_value)


# A Publish Requirement for a related ClusterableModel
class RelationPublishRequirement(BasePublishRequirement):
    def __init__(self, field_name, criteria=has_at_least_one, message=placeholder_message):
        self.field_type = "relation"
        self.field_name = field_name
        self.criteria = criteria
        self.message = message

    def check_criteria(self, form):
        field_name = self.field_name
        formsets = form.formsets
        if field_name in formsets:
            formset_errors = formsets.get(field_name).errors
            # formset_errors is a list of dictionary of errors
            # if there are no errors, the list = [{}] (still has length)
            if len(formset_errors) == 0 or all(not bool(error) for error in formset_errors):
                data = formsets.get(field_name).cleaned_data
                return self.evaluate(field_name, data)
            else:
                return publish_error_factory(
                    field_name,
                    self.field_type,
                    self.message,
                )
        else:
            raise KeyError(f"Field required for publish '{field_name}' does not exist.")


class ConditionalPublishRequirement(BasePublishRequirement):
    def __init__(self, requirement1, operation, requirement2, message=placeholder_message):
        self.requirement1 = requirement1
        self.operation = self.operation_map[operation]
        self.requirement2 = requirement2
        self.message = message

    operation_map = {
        "or": lambda a,b: a or b,
        "and": lambda a,b: a and b,
    }

    def check_criteria(self, form):
        result1 = self.requirement1.check_criteria(form)
        result2 = self.requirement2.check_criteria(form)
        if not self.operation(
            result1["passed"],
            result2["passed"],
        ):
            conditional_result = {
                "passed": False,
                "publish_requirement_errors": [],
            }
            for result in (result1, result2):
                if not result["passed"]:
                    for error in result["publish_requirement_errors"]:
                        # Use message from ConditionalPublishRequirement
                        # if nested PublishRequirement did not specify a message
                        if not error.publish_error_data["message"]:
                            error.publish_error_data["message"] = self.message
                        conditional_result["publish_requirement_errors"].append(error)
            return conditional_result
        else:
            return publish_success_factory()


class StreamFieldPublishRequirement(BasePublishRequirement):
    """Publishing Requirement for Streamfields"""
    def __init__(self, field_name, criteria=streamfield_has_length, message=placeholder_message, langs=None):
        self.field_type = "streamfield"
        self.field_name = field_name
        self.criteria = criteria
        self.message = message
        self.langs = langs

    def check_criteria(self, form):
        """
        Goes through form looking for the field_name, appending the appropriate language tag to end of field_name
        if self.langs. Calls self.evaluate if field_name exists, otherwise returns a PublishRequirementError
        If the streamfield is missing elements, the form does not include it in cleaned_data.
        :param form: form being checked
        :return: result of self.evaluate
        """
        field_name = self.field_name
        data = form.cleaned_data
        # If field is translated, then check value of each applicable language
        if self.langs:
            for lang in self.langs:
                translated_field_name = f'{self.field_name}_{lang}'
                if translated_field_name in data:
                    field_value = data.get(translated_field_name)
                    return self.evaluate(translated_field_name, field_value)
                else:
                    # if the section doesnt have a header and a page attached, the section isn't added to the
                    # cleaned_data at all
                    return publish_error_factory(
                        field_name,
                        self.field_type,
                        self.message,
                    )
        else:
            # If field is not translated, then get check value of "field_name"
            field_value = data.get(field_name)
            return self.evaluate(field_name, field_value)


# A Publish Requirement for departments
class DepartmentPublishRequirement(BasePublishRequirement):
    def __init__(self, message=placeholder_message):
        self.message = message

    def check_criteria(self, form):
        page = form.instance
        group_page_permissions = page.group_permissions.all()

        # If we have a department group with a department page, SUCCESS!
        for group_page_permission in group_page_permissions:
            # Department groups have this
            if hasattr(group_page_permission.group, "department"):
                department_page = group_page_permission.group.department.department_page
                if department_page:
                    return publish_success_factory()

        # If we've made it here, it means we didn't find what we were looking for, FAILURE
        return publish_error_factory('departments', 'department', 'missing department page')
