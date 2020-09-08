# MovieRama

Yet another social platform app where users can share their favorite movies.

## Quick installation guide

Install python (preferably v3.8).
> <a href="https://realpython.com/installing-python/">Here</a> you can find additional information about python installation.

Navigate to the projects root directory (movierama).

Create and activate a python virtual environment.
> python3 -m venv venv

> source venv/bin/activate

Install the project's requirements.

> pip install -r requirements.txt

#
For convenience the default django sqlite3 database has been user. This database requires no installation, 
just migrate the models by typing
> python3 manage.py migrate

In order to create some additional data you can execute the following command inside project's root directory.
> python3 manage.py initialdatagenerator

More information about how the data are generated you can find by navigating to 
> movies/management/commands/initialdatagenerator.py

# 
Start django server by typing
> python3 manage.py runserver

Access the application by typing the following url in any browser, create an account and start submitting your 
favorite movies..
> http://127.0.0.1:8000/


## Tests 
25 tests are included in order to validate some basic functionality. To execute the tests type:
> python3 manage.py test
