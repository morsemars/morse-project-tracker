# Morse Project Tracker

## Introduction

The Morse Project Tracker or MPT is a project management app targeted to keep track of the progress of my side projects. 

This is made mainly to improve my skills as a full-stack developer. This will ensure that I will be able to add new features while making sure that the application is still usable.

## Getting Started

### Installing Dependencies

#### Python 3

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is used to handle cross origin requests from the front-end server. 

#### Installing Dependencies and Running the Server Locally

Make sure to install Flask first.

`pip3 install Flask`

After installing Flask globally, follow the instructions below:

1. Create a new virtual environment.
    ```
    $ cd <project_directory>
    $ python3 -m venv env
    $ source env/bin/activate
    ```

2. Install dependencies.

    `$ pip install -r requirements.txt`

3. Run the development server.

    `./start_dev.sh`

    or 

    ```
    $ export FLASK_APP=mpt
    $ export FLASK_ENV=development
    $ flask run
    ```
4. Go to http://127.0.0.1:5000/

## Database Setup
With Postgres running, populate the database using the mpt.psql file provided and then run the following command:
```
$ psql project_tracker < mpt.psql
```

## Testing the Application
On the root directory, run the following commands:

```
$ dropdb mpt_test
$ createdb mpt_test
$ psql mpt_test < mpt.psql
$ python3 -m unittest discover tests -p *_test.py -v
```

## API Endpoints

### Users

GET /users
- Fetches the list of users currently registered in the application.
- Permission: "get:users"
- Returns: 
```

```

POST /users
- Permission: "post:users"

GET /users/{id}
- Permission: "get:users"

PATCH /users/{id}
- Permission: "patch:users"

DELETE /users/{id}
- Permission: "delete:users"

GET users/{id}/projects
- Fetches all the projects where the user is assigned.
- Permission: "get:projects"

GET users/{id}/tasks
- Fetches all the task assigned to the user.

### Projects

GET /projects
- Fetches a list of registered projects.
- Request Arguments: None

- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 

POST /projects

GET /projects/{id}

PATCH /projects/{id}

DELETE /projects/{id}

### Tasks

GET /tasks
- Fetches all tasks
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 

POST /tasks

GET /tasks/{id}

PATCH /tasks/{id}

DELETE /tasks/{id}

### Activities

GET /activities
- Fetches a list of activities.
- Request Arguments: None

- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 

POST /activities

GET /activities/{id}

PATCH /activities/{id}

DELETE /activities/{id}




