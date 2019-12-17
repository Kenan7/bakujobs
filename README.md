#  Setting Up for Development


* install dependencies (Debian/Ubuntu)

        $ sudo apt-get update
        $ sudo apt-get install -y gcc python3-dev python3-venv

* prepare directory for project code and virtualenv:

        $ mkdir -p ~/webapps
        $ cd ~/webapps

* download the project code:

        $ git clone https://github.com/Kenan7/bakujobs.git
* go in to the project dir:

        $ cd bakujobs
        
* prepare virtual environment
  (with virtualenv you get pip, we'll use it soon to install requirements):

        $ python3 -m venv env
        $ source env/bin/activate


* install requirements (Django, ...) into virtualenv:

        $ pip install -r requirements.txt
        
* Make migrations:

        $ (env) python manage.py makemigrations
        
* Build the database:

        $ (env) python manage.py migrate

* Create a superuser:

        $ (env) python manage.py createsuperuser


* Run the development server:

        $ (env) python manage.py runserver





