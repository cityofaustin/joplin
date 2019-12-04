import subprocess, re, os, sys, json, time

APPNAME = sys.argv[1]

def check_app_status():
    print(f"Checking state of App {APPNAME}.")
    output = subprocess.run(re.split("\s+", f"heroku ps -a {APPNAME} --json"),
        capture_output=True,
        text=True
    )
    if (output.stderr):
        print(output.stderr)
        sys.exit(1);
    app_info = json.loads(output.stdout)
    app_state = app_info[0]['state']
    if (app_state == 'up'):
        print(f"App {APPNAME} is up. Ready to migrate.")
        return
    elif (app_state == 'starting'):
        print(f"App {APPNAME} is still starting up. Trying again")
        time.sleep(1)
        check_app_status()
    else:
        print(f"Error: App {APPNAME} is in state {app_state}")
        sys.exit(1);

check_app_status()
