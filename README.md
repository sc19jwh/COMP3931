# COMP3931 Individual Project

This is the code repository for COMP3931 Individual Project by Jack Howkins (sc19jwh).

This repository includes all project files besides 2x API private keys - the application will still function without these keys but will not have access to the features that require API access. The project has been deployed to <a href="railwizard.python.anywhere.com" target="_blank">railwizard.python.anywhere.com</a> with full API functionality - this is the easiest way to access and use the web application.

Build instructions for running the web application locally are included below.

# Build Instructions

1. Clone this repository
2. Create a virtual environment using `python -m virtualenv venv`
3. Activate the virtual environment using `source venv/bin/activate` (Linux) or `venv\Scripts\activate` (Windows)
4. Install the requirements using `pip install -r requirements.txt`
5. __OPTIONAL__: Run `npm run build` to build the tailwindcss files (this step is only necessary if making source code changes, the included output.css file in the repository is otherwise up to date with all styling) 
6. Run `python manage.py runserver` to start the application - you will then be able to access the web application at port number 8000 (or at the alternative port number chosen).
7. __OPTIONAL__: Additionally, `python manage.py test apps` can be used to run the included unit tests. Running `python manage.py test apps/<app_name>` will run the unit tests for an individual Django app.
