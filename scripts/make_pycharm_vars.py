# Convert the values of your .env file into a single line of environment variables to plug into Pycharm run configuration.
# pipenv run python scripts/make_pycharm_vars.py
import os
from os import path
import re
env = open(path.join(path.dirname(__file__), '../.env'), "r")

pycharm_vars = ""
for line in env.readlines():
    if not line.startswith("#"):
        line = line.strip()
        if line:
            var_name = re.match(r'(.*)\=', line)[1]
            pycharm_vars = pycharm_vars + var_name + "=" + os.getenv(var_name) + ";"

print(pycharm_vars)
