## Instagram

#Instagram clone
2019

### By Shirley Keter

## Description
This is a clone of the instagram website. A user can create an account and sign into it. The site supports uploading images, and following other users.Users can also view photos uploaded by other users in the home page of app.


## Set Up and Installations

### Prerequisites
* Ubuntu Software
* Python3.6
* Postgres
* python virtualenv
* Clone the Repo
* Run the following command on the terminal: git clone https://github.com/chiriket/Instagram.git && cd Instagram

### Activate virtual environment
Activate virtual environment using python3.6 as default handler

virtualenv -p /usr/bin/python3.6 venv && source venv/bin/activate

Install dependancies
Install dependancies that will create an environment for the app to run pip3 install -r requirements.txt

### Create the Database
* psql
* CREATE DATABASE insta;

### Create .env file.

### Run initial Migration
python3.6 manage.py makemigrations gram
python3.6 manage.py migrate
Run the app
python3.6 manage.py runserver
Open terminal on localhost:8000

## Known bugs
There are no known bugs.

## Technologies used
- Python 3.6
- HTML
- Bootstrap 4
- JavaScript
- Heroku
- Postgresql

## Support and contact details
Contact me on shirleyketer@gmail.com.

## License
Copyright (c) Shirley Keter