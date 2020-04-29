# Morse Project Tracker

## Introduction

The Morse Project Tracker or MPT is a project management app targeted to keep track of the progress of my side projects. 

This is made mainly to improve my skills as a full-stack developer. This will ensure that I will be able to add new features while making sure that the application is still usable.

URL: http://morse-project-tracker.herokuapp.com/

## Getting Started

### Installing Dependencies

#### Python 3

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is used to handle cross origin requests. 

#### Installing Dependencies and Running the Server Locally

Make sure to install Flask first.

`pip3 install Flask`

After installing Flask globally, follow the instructions below:

1. Create a new virtual environment.
    ```
    cd <project_directory>
    python3 -m venv env
    source env/bin/activate
    ```

2. Install dependencies.

    `pip install -r requirements.txt`

3. Setup Auth0
    - create an .env file and fill with your own Auth0 details. (Please see .env.example)
    - create roles Manager and Developer. The permissions are listed in the [Roles](#Roles) section below.

4. Setup Database. (See [Database Setup](#database-setup))

4. Run the development server.

    `./start_dev.sh`

    or 

    ```
    export FLASK_APP=mpt
    export FLASK_ENV=development
    flask run
    ```
5. Go to http://127.0.0.1:5000/

## Database Setup
1. Create database tables.
    ```
    python3 manage_db.py db migrate
    ```
2. Populate database with test values.
    ```
    psql project_tracker < mpt.psql
    ```

## Testing the Application

### Python Unit Test
On the root directory, run the following commands:

1. Login to the Application: http://127.0.0.1:5000/login, then copy the token to config.py inside the tests folder.

    - Login as a Manager then paste token to TOKEN.
        - e-mail: manager@mpt.com
        - password: Mpt_Manager

    - Login as a Developer then paste token to DEV_TOKEN.
        - e-mail: dev@mpt.com
        - password: Mpt_Developer

2. Type the following commands in the project's root folder

    ```
    dropdb mpt_test
    createdb mpt_test
    python3 create_test_db.py
    psql mpt_test < mpt.psql
    python3 -m unittest discover tests -p *_test.py -v
    ```

### Postman 

1. On postman, import mpt.postman.json
2. Login to the Application: http://127.0.0.1:5000/login, then update bearer token.

    - Login as a Manager, then edit the ___Manager___ folder. Set the Type as _Bearer Token_ on the Authorization tab and then paste the token.

    - Login as a Developer, then edit the ___Developer___ folder. Set the Type as _Bearer Token_ on the Authorization tab and then paste the token.

3. Click Runner, select mpt then click "Run mpt"

    __NOTE__: You can update the "host" variable in the collection to test your local setup.

## Roles

1. Developer

    - get:projects
    - get:tasks
    - get:activities
    - get:users
    - post:activities
    - patch:activities
    - patch:tasks
    - delete:activities

2. Manager
    - get:projects
    - get:tasks,
    - get:activities
    - get:users
    - post:projects
    - post:tasks
    - post:users
    - patch:projects
    - patch:tasks
    - patch:users
    - delete:projects
    - delete:tasks
    - delete:users

## API Endpoints

### Users

| API Endpoint | URL Parameters | Data Parameters | Description |
| --- | --- | --- | --- |
| GET /users | | | Fetches the list of users currently registered. |
| POST /users | | __first_name__: String <br> __last_name__: String <br> __position__: String -  Manager or Developer  | Registers a new user as a Manager or Developer. |
| GET /users/:id | | | Fetches  the user details|
| PATCH /users/id | | __first_name__: String <br> __last_name__: String <br> __position__: String -  Manager or Developer   | Updates user details. |
| DELETE /users/:id | | | Deletes a user. |
| GET /users/:id/projects  | | | Fetches the list of projects the user has been assigned to. |
| GET /users/:id/tasks  | | | Fetches the list of tasks the user is handling. |


### Projects

| API Endpoint | URL Parameters | Data Parameters | Description |
| --- | --- | --- | --- |
| GET /projects | | | Fetches all projects. | get:projects |
| POST /projects | | __name__: String <br> __description__: String <br> __manager__: Integer - id of the manager <br> __status__: String <br> __assignees__: [Integer] - list of developer ids | Add a new project. |
| GET /projects/:id | | | Fetches  the project details|
| PATCH /projects/:id | |  __name__: String <br> __description__: String <br> __manager__: Integer - id of the manager <br> __status__: String <br> __assignees__: [Integer] - list of developer ids | Updates project details. |
| DELETE /projects/:id | | | Deletes a project. |
| GET /projects/:id/tasks | | | Fetches  the tasks of a project |


### Tasks

| API Endpoint | URL Parameters | Data Parameters | Description |
| --- | --- | --- | --- |
| GET /tasks | | | Fetches all tasks. |
| POST /tasks | | __name__: String <br> __description__: String <br> __status__: String <br> __project__: Integer - project id <br> __assignee__: Integer - user id of the developer assigned. | Add a new task. |
| GET /tasks/:id | | | Fetches  the task details|
| PATCH /tasks/:id | | __name__: String <br> __description__: String <br> __status__: String <br> __project__: Integer - project id <br> __assignee__: Integer - user id of the developer assigned. | Updates task details. |
| DELETE /tasks/:id | | | Deletes a task. |
| GET /tasks/:id/activities | | | Fetches  the task details |

### Activities

| API Endpoint | URL Parameters | Data Parameters | Description |
| --- | --- | --- | --- |
| GET /activities | | | Fetches all activities. |
| POST /activities | | __task_id__: Intger <br> __description__: String - activity description <br> __hours__: Integer | Add a new activity. |
| GET /activities/:id | | | Fetches  the activity details|
| PATCH /activities/:id | | __description__: String - activity description <br> __hours__: Integer | Updates activity details. |
| DELETE /activities/:id | | | Deletes a activity. |



