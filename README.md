# Moneyball project

## Django setup
* Install `virtualenv` using `pip`
    * `pip install virtualenv`
* Create virtual environment:
    * `virtualenv venv`
* Activate the virtual environment:
    * `source venv/bin/activate`
* Install `pip` packages:
    * `pip install -r requirements.txt`
    * For Mac OS X: `pip install -r requirements-Mac.txt`

## Useful links
* [Markdown tutorial](https://bitbucket.org/tutorials/markdowndemo/overview)
* [Django documentation](https://docs.djangoproject.com/en/1.6/)
* [Django/Heroku setup](https://devcenter.heroku.com/articles/getting-started-with-django)

## Django Social Authentication
* [django-social-auth](http://django-social-auth.readthedocs.org/en/latest/index.html)
* [Step-by-step tutorial: Django Social Auth](http://c2journal.com/2013/01/24/social-logins-with-django/)


## Yahoo login added conf
* add following line in /etc/ports.conf
mywebsite.com 127.0.0.1
* run the server in port 80, need super user permit
$ python manage.py runserver 80
* in facebook, allowed site(mobile site) I have added 'mywebsite.com'
=======
