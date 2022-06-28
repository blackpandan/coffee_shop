# **COFFEE APP**

## **INTRODUCTION**
---
coffee shop is a web app that allows user to create, delete and edit drinks, it authenticates users using auth0 and connects to an api made using flask.

the backend was created with python flask following [pep8 guidelines]().

the frontend was made with angular, ionic and typescript.

---
## **GETTING STARTED**
---
## **Perequisites & Installation**
packages need to be installed in order to get the app running, backend dependecies are installed using pip and frontend npm

### **Backend**
- install python if it's not installed from the [official website](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

- create a virtual environment in other to have an isolated system more info [here](https://docs.python.org/3/library/venv.html#:~:text=A%20virtual%20environment%20is%20a,part%20of%20your%20operating%20system.)

- change directory to backend, install dependencies using pip
    ```
    pip install -r requirements.txt
    ```

- now to get the flask server running, if you intend to run it in a development environment, export the flask_env and flask_app variables first, change directory to backend/src

    for window cmd
    ```
    set FLASK_APP=api.py
    set FLASK_ENV=development
    ```
    for window powershell
    ```
    $Env:FLASK_APP=api.py
    $Env:FLASK_ENV=development
    ```
    for linux
    ```
    export FLASK_APP=api.py
    export FLASK_ENV=development
    ```

- finally run the server with

   ```
    flask run
   ```

### **Frontend**

- install npm page manager and node runtime environment from [here](https://nodejs.com/en/download).

- install ionic ( needed to run serve the frontend ) from [here](https://ionicframework.com/docs/intro/cli).

- to install project dependencies change directory to frontend and run
    ```bash
    npm install 
    ```

- you would need to change variables in ``` ./src/environments/environments.ts``` to match your own

- finally run the project in dev mode with ssl support using

    ```bash
    ionic serve --ssl
    ```

### **setup auth0**

- create an account, application and api on [auth0](https://auth0.com)

- enable RBAC for the account 

---
### **Test**
---
download and install [postman](https://getpostman.com/) into order to run tests


- import the postman collection from ```./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json```

- you would need to register 