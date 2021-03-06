# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also the [TRELLO_KEY](https://developer.atlassian.com/cloud/trello/rest/api-group-actions/) and [TRELLO_TOKEN](https://developer.atlassian.com/cloud/trello/rest/api-group-actions/) variables which are used to authorize the trello board api requests. Please make sure you enter all values into the environment variables file.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```

## Testing the Application

Once you have installed all the dependencies and initialised all the environment variables, you can run the testing suites by running:
```bash
$ poetry run pytest
```

To run individual tests, please use the following command:
```bash
$ poetry run pytest PATH\TO\<FILE_NAME>
```

## Selenium Testing

To enable selenium to work, you need to follow the instructions below to enable selenium to use chrome to begin testing:
1: [ChromeDriverWebsite](https://chromedriver.chromium.org/)
2: [Setup Instructions](https://www.browserstack.com/guide/run-selenium-tests-using-selenium-chromedriver)

If you are using WSL2 or a VM to run a Unix Distro, make sure you have a GUI service like [VcXsrv](https://sourceforge.net/projects/vcxsrv/) to show a GUI for selenium to load if you are ssh'ed in
You would also need the following display environment property in your bash / zsh profile:
```
$ export DISPLAY=$(ip route | awk '{print $3; exit}'):0
```

Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Docker

This application has a dockerfile and can be run if you have Docker installed.
As a pre-requisite please make sure to install Docker from (HERE)[https://docs.docker.com/get-docker/]

There are 2 configurations that are possible to run, a production environment build and a development build. In order to proceed to this next step please make sure that you have followed the previous steps and have verified that the application can run locally (assuming the secrets `.env` has been correctly populated).
Once this has been confirmed, to build the docker image please run:

For development:

```bash
$ docker build --target development --tag todo-app:dev .
```

For production:
```bash
$ docker build --target production --tag todo-app:prod .
```

Then to run the image use:

```bash
$ docker run --env-file .env -p 8000:8000 todo-app:dev
```
(Replacing dev with prod as appropriate)


Now visit [`http://localhost:8000/`](http://localhost:8000/) in your web browser to view the app.
