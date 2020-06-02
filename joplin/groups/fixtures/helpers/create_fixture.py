from groups.models import Department
from groups.factories import DepartmentFactory


# Skips creating fixture if Group with name already exists
def create_fixture(group_data, fixture_name):
    try:
        group = Department.objects.get(name=group_data['name'])
    except Department.DoesNotExist:
        group = None
    if group:
        print(f"Skipping {fixture_name}")
        return group

    group = DepartmentFactory.create(**group_data)
    print(f"Built {fixture_name}")
    return group
