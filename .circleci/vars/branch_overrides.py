'''
    This is where you set environment variables that you want to set specifically for
    your PR branch only.
    The key is your git branch name.
    Within that branch name, set the environment vars that you'd like to override.
    Whatever you set in that object will not contaminate the environment vars of any other branch.
    You're allowed to override any environment var (even ones in vars_from_circleci),
    though you probably don't want to.
    branch_overrides are not required for every branch.
'''
branch_overrides = {
    "3218-go-fast": {
        # "DEBUG_TOOLBAR": True,
        # "DEBUG": 1,
    },
    "4224-resolve-dept": {
        "LOAD_DATA": "",
        "V3_WIP": True,
    },
    "v3": {
        "LOAD_DATA": "dummy",
        "V3_WIP": True,
    },
    "4148-add-homepage": {
        "LOAD_DATA": "",
        "V3_WIP": True,
    },
    "4047-separate-groups": {
        "LOAD_DATA": "dummy",
        "V3_WIP": True,
    },
    "4165-streamfields": {
        "LOAD_DATA": "",
        "V3_WIP": True,
    },
    "4165-service-page-tests": {
        "LOAD_DATA": "dummy",
        "V3_WIP": True,
    }
}
