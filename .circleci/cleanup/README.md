Wow! We now have a way to automatically close Heroku apps after they've been merged in or closed on github.

To redeploy this lambda function:
1. Make sure you've got a valid GITHUB_WEBHOOK_SECRET_TOKEN and HEROKU_KEY in your .env file.
2. Run `sh ./.circleci/cleanup/deploy.sh`
