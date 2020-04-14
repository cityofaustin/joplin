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
    "4273-correct-ids": {
        "LOAD_DATA": "",
        "V3_WIP": True,
    },
    "v3": {
        "LOAD_DATA": "fixtures",
        "V3_WIP": True,
    },
    "not-top-pages-topics": {
        "LOAD_DATA": "fixtures",
        "V3_WIP": True,
    },
    "4266-guide": {
        "LOAD_DATA": "fixtures",
        "V3_WIP": True,
    },
    "base-content-type": {
        "LOAD_DATA": "fixtures",
        "V3_WIP": True,
    },
    "test-pr-build": {
        "LOAD_DATA": "fixtures",
        "V3_WIP": True,
    }
}
