import os, json

zappa_settings = {
  "staging": {
    "project_name": "coa-joplin-build-cleanup",
    "s3_bucket": "coa-zappa-build",
    "app_function": "main.app",
    "runtime": "python3.7",
    "profile_name": "default",
    "environment_variables": {
      "GITHUB_WEBHOOK_SECRET_TOKEN": os.getenv("GITHUB_WEBHOOK_SECRET_TOKEN"),
      "HEROKU_KEY": os.getenv("HEROKU_KEY"),
    }
  }
}

zappa_settings_file = os.path.join(os.path.dirname(__file__), 'zappa_settings.json')
with open(zappa_settings_file, 'w+', encoding='utf-8') as outfile:
    json.dump(zappa_settings, outfile, ensure_ascii=False, indent=4)
