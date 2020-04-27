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
1. Create database tables.
    ```
    $ python3 manage_db.py db migrate
    ```
2. Populate database with test values.
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

| API Endpoint | URL Parameters | Data Parameters | Description | Permissions |
| --- | --- | --- | --- | --- |
| GET /users | | | Fetches the list of users currently registered. | get:users |
| POST /users | | _first_name_: String <br> _last_name_: String <br> _position_: String -  Manager or Developer  | Registers a new user as a Manager or Developer. | post:users |
| GET /users/:id | | | Fetches  the user details| get:users |
| PATCH /users/id | | _first_name_: String <br> _last_name_: String <br> _position_: String -  Manager or Developer   | Updates user details. | patch:user |
| DELETE /users/:id | | | Deletes a user. | delete:user |
| GET /users/:id/projects  | | | Fetches the list of projects the user has been assigned to. | get:projects |
| GET /users/:id/tasks  | | | Fetches the list of tasks the user is handling. | get:tasks |


### Projects

| API Endpoint | URL Parameters | Data Parameters | Description | Permissions |
| --- | --- | --- | --- | --- |
| GET /projects | | | Fetches all projects. | get:projects |
| POST /projects | | _name_: String <br> _description_: String <br> _manager_: Integer - id of the manager <br> _status_: String <br> _assignees_: [Integer] - list of developer ids | Add a new project. | post:projects |
| GET /projects/:id | | | Fetches  the project details| get:projects |
| PATCH /projects/:id | |  _name_: String <br> _description_: String <br> _manager_: Integer - id of the manager <br> _status_: String <br> _assignees_: [Integer] - list of developer ids | Updates project details. | patch:project |
| DELETE /projects/:id | | | Deletes a project. | delete:project |
| GET /projects/:id/tasks | | | Fetches  the tasks of a project | get:tasks |


### Tasks

| API Endpoint | URL Parameters | Data Parameters | Description | Permissions |
| --- | --- | --- | --- | --- |
| GET /tasks | | | Fetches all tasks. | get:tasks |
| POST /tasks | | _name_: String <br> _description_: String <br> _status_: String <br> _project_: Integer - project id <br> _assignee_: Integer - user id of the developer assigned. | Add a new task. | post:tasks |
| GET /tasks/:id | | | Fetches  the task details| get:tasks |
| PATCH /tasks/:id | | _name_: String <br> _description_: String <br> _status_: String <br> _project_: Integer - project id <br> _assignee_: Integer - user id of the developer assigned. | Updates task details. | patch:task |
| DELETE /tasks/:id | | | Deletes a task. | delete:task |
| GET /tasks/:id/activities | | | Fetches  the task details| get:activities |

### Activities

| API Endpoint | URL Parameters | Data Parameters | Description | Permissions |
| --- | --- | --- | --- | --- |
| GET /activities | | | Fetches all activities. | get:activities |
| POST /activities | | _task_id_: Intger <br> _description_: String - activity description <br> _hours_:Integer | Add a new activity. | post:activities |
| GET /activities/:id | | | Fetches  the activity details| get:activities |
| PATCH /activities/:id | | _description_: String - activity description <br> _hours_:Integer | Updates activity details. | patch:activity |
| DELETE /activities/:id | | | Deletes a activity. | delete:activity |



