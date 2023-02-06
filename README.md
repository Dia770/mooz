# Backend - Tontine API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment**

- We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

- Read how_to_create_a_virtual_env.txt in help folder to create and activate the virtual env named "virtualenv"

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by running in this directory:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With mysql create a `tontine_app` database. You can use a XAMPP server, you can read [install-mysql-and-phpmyadmin-with-xampp]https://www.jcchouinard.com/install-mysql-and-phpmyadmin-with-xampp/ to get started

### Database migration

To initialize the migration file, execute :

```bash
export FLASK_APP=main.py
flask db init
```

To upgrade the database to the last state of models.py , execute (`export FLASK_APP=main.py` is required):

```bash
flask db migrate
flask db upgrade
```

### Run the Server

From this directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=main.py
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

The server will run on `127.0.0.1:5000`

## API endpoints cocumentation

`POST '/sign-up'`

- Create a new user
- Request Arguments:

```json
{
  "first_name": "Amadou",
  "last_name": "Diallo",
  "card_number": "P-48795129",
  "telephone": "+223 90442359",
  "password": "mypass"
}
```

- Returns in "data": all the info of the new user except the password and the user_id, and a token that contains his `user_id:` and that will help him use the login required routes

```json
{
  "code": 200,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMmMxMzA3ZHF0bnZ1MyIsInBob25lIjoiKzIyMyA5MDQ0MjM1OSIsImV4cCI6MTY3NTU5OTg0M30._NuB9lgVF0yQRZ5-fNoYxddF0o9FzwnxaDc_taTWCvA",
    "user": {
      "card_number": "48795129",
      "card_type": "Passport",
      "first_name": "Amadou",
      "id": 6,
      "last_name": "Diallo",
      "password": null,
      "telephone": "+223 90442359"
    }
  },
  "detail": "user successfully created",
  "message": "user_created",
  "success": true
}
```

`POST '/login'`

- Connect a user
- Request Arguments:

```json
{
  "con_telephone": "+223 90442359",
  "con_password": "mypass"
}
```

- Returns in "data": all the info of the new user except the password and the user_id, and a token that contains his `user_id:` and that will help him use the login required routes

```json
{
  "code": 200,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMmMxMzA3ZHF0bnZ1MyIsInBob25lIjoiKzIyMyA5MDQ0MjM1OSIsImV4cCI6MTY3NTU5OTg0M30._NuB9lgVF0yQRZ5-fNoYxddF0o9FzwnxaDc_taTWCvA",
    "user": {
      "card_number": "48795129",
      "card_type": "Passport",
      "first_name": "Amadou",
      "id": 6,
      "last_name": "Diallo",
      "password": null,
      "telephone": "+223 90442359"
    }
  },
  "detail": "user successfully connected",
  "message": "user_verified",
  "success": true
}
```

## Testing

To deploy the tests, run

```bash
python test_flaskr.py
```
