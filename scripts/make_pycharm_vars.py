# Convert the values of your .env file into a single line of environment variables to plug into Pycharm run configuration.
# pipenv run python scripts/make_pycharm_vars.py

from os import path
env = open(path.join(path.dirname(__file__), '../.env'), "r")

pycharm_vars = ""
for line in env.readlines():
    if not line.startswith("#"):
        pycharm_vars = pycharm_vars + line.strip() + ";"

print(pycharm_vars)
