# Grumblr-Web-Application
A Blogging-like Web Application

How to run this project:
For directories from 1 to 4, run the following commands:

    $ cd dir
    $ python manage.py makemigrations
    $ python manage.py migrate
    $ python manage.py runserver

Open your browser and navigate yourself to http://127.0.0.1:8000/

For directory named `5`, it was deployed onto AWS EC2. Data was stored in S3.
One can use the configuration files provided inside the directory to deploy this project onto AWS.
