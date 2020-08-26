# Contains python and circleci prereqs
FROM circleci/python:3.7.5-stretch

# Install nodejs
RUN curl -sL https://deb.nodesource.com/setup_10.x | sudo bash -
RUN sudo apt-get update; sudo apt-get -y install nodejs
RUN sudo npm install --global yarn

# Install pipenv
RUN sudo pip install pipenv
