[![Build Status](https://travis-ci.org/muthash/Weconnect-api.svg?branch=feedback)](https://travis-ci.org/muthash/Weconnect-api)
[![Coverage Status](https://coveralls.io/repos/github/muthash/Weconnect-api/badge.svg?branch=feedback&service=github)](https://coveralls.io/github/muthash/Weconnect-api?branch=feedback&service=github)
[![Maintainability](https://api.codeclimate.com/v1/badges/0f8371ef14ba3dc4fa04/maintainability)](https://codeclimate.com/github/muthash/Weconnect-api/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/689e408250dd44fdb62c3ca38cd8aa0d)](https://www.codacy.com/app/muthash/Weconnect-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=muthash/Weconnect-api&amp;utm_campaign=Badge_Grade)

# WeConnect

This is an API for WeConnect, a platform that brings businesses and individuals together. This platform creates awareness for businesses and gives the users the ability to:

- Register for an account
- Login into registered account
- Reset forgotten password
- Change password
- Delete user account
- Register, Update and Delete a Business
- View all Businesses
- View single Business
- Write Reviews on a business
- View all Reviews to a business
- Search and filter businesses

## Prerequisites

- Python 3.6 or a later version
- PostgreSQL

## Installation

Clone the repo.
```
$ git clone https://github.com/muthash/Weconnect-api.git
```
and cd into the folder:
```
$ /WeConnect-api
```

## Virtual environment

Create a virtual environment:
```
virtualenv venv
```
Activate the environment
```
$ source venv/bin/activate
```

## Dependencies

Install package requirements to your environment.
```
pip install -r requirements.txt
```

## Env

Create a .env file in your Weconnect-api  root directory and add
```
source venv/bin/activate
export FLASK_APP="run.py"
export SECRET="some-very-long-string-CHANGE-TO-YOUR-LIKING"
export APP_SETTINGS="production"
export DATABASE_URL="postgresql://username:password@localhost/wc_db"
export TEST_DATABASE_URL="postgresql://username:password@localhost/test_wc_db"
export EMAIL="email-address-to-use-to-send-mails"
export PASSWORD="password-for-above-email"
```

activate the environment
```
source .env
```

## Database migration

Create two Databases in PostgreSQL:
- wc_db (production DB)
- test_wc_db (testing DB)

Run the following commands for each database:
```
python manager.py db init

python manager.py db migrate

python manager.py db upgrade

```

## Testing

To set up unit testing environment:
```
$ pip install nose
$ pip install coverage
```

To run tests perform the following:
```
$ nosetests --with-coverage
```

## Start The Server

To start the server run the following command
```
flask run
```
The server will run on http://127.0.0.1:5000/

## Testing API on Postman

*Note* Ensure that after you succesfully login a user, you use the generated token in the authorization header for the endpoints that require authentication. Remeber to add Bearer before the token as shown:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9eyJpYXQiO 
```

### API endpoints

| Endpoint | Method |  Functionality | Authentication |
| --- | --- | --- | --- |
| /api/v1/register | POST | Creates a user account | FALSE
| /api/v1/login | POST | Logs in a user | TRUE
| /api/v1/logout | POST | Logs out a user | TRUE
| /api/v1/reset-password | POST | Reset user password | TRUE
| /api/v1/change-password | PUT | Change user password | TRUE
| /api/v1/delete-account | POST | Delete user password | TRUE
| /api/v1/businesses | POST | Register a business | TRUE
| /api/v1/businesses | GET | Retrieves all businesses | OPTIONAL 
| /api/v1/businesses/{businessid} | GET | Retrieve a single business | OPTIONAL
| /api/v1/businesses/{businessid} | PUT | Update a business profile | TRUE
| /api/v1/businesses/{businessid} | DELETE | Delete a business | TRUE
| /api/v1/businesses/{businessid}/reviews | POST | Post a review on a business | TRUE
| /api/v1/businesses/{businessid}/reviews | GET | Get all reviews to a business | OPTIONAL
| /api/v1/search | GET | Search and filter businesses | OPTIONAL

## Pagination

The API enables pagination by passing in *page* and *limit* as arguments in the request url as shown in the following example:

```
http://127.0.0.1:5000//api/v1/businesses?page=1&limit=20

```

## Searching and filtering

The API implements searching based on the name using a GET parameter *q* as shown below:
```
http://127.0.0.1:5000//api/v1/search?q=Andela
```
One can also filter a search result further based on the business location and category as shown:
```
http://127.0.0.1:5000//api/v1/search?q=Andela&cat=Tech&loc=Nairobi
```

## Heroku Production Link

```
https://wc-app-api.herokuapp.com/

```

## API Documentation

[Apiary API documentation](https://weconnect15.docs.apiary.io/#)

## Authors

* **Stephen Muthama** - [muthash](https://github.com/muthash)

## Acknowledgments
* Kelvin Munene - [kmunene](https://github.com/kmunene)
