## Notes:
Updated the requirements.txt for compatibility issue

## For running tests and coverage (to avoid including site-wide packages due to virtual env)
cd into project directory
coverage run manage.py test
coverage html --include=./*  