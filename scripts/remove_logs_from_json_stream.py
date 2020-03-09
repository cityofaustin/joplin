import re
import sys
import fileinput

'''
    The "datadump" command might pipe over deprecation warning messages from python.
    This script removes those warning messages from the data pipe stream.

    "[" marks the beginning of a json file. Any line before this line is a message, and not part of our json data.
    Any line after [ will be part of the json file.

    TODO: Making sure to update python dependencies before pushing to production would eliminate the need for this script.
'''

start_of_json_pattern = re.compile("^\[")
end_of_json_pattern = re.compile("^\]")
in_json = False

for line in fileinput.input():
    if end_of_json_pattern.match(line):
        sys.stdout.write(line)
        in_json = False
    elif in_json:
        sys.stdout.write(line)
    elif start_of_json_pattern.match(line):
        in_json = True
        sys.stdout.write(line)
