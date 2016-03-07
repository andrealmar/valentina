# Valentina 

WIP (i.e. work in progress), but feel free to get in touh and join us.

## Install

### Requirements

We use [Django](http://djangoproject.com) in the backend and [React](http://reactjs.com) in the frontend. We also use [Bower](http://bower.io) to manage some assets requirements.

That said these are the requirements:

* [Python](http://python.org) 3.5 with `pip` ([virtualenv](http://virtualenv.readthedocs.org) recommended)
* [Node.js](http://nodejs.org/) 5.x with `npm`

### Dependencies

Once you have `pip` and `npm` available let's install the dependencies:

```
pip install -r requirements.txt
npm install
bower install
```

### Facebook settings

In order to use Facebook OAuth, create a app as a [developer at Facebook](http://developers.facebook.com) and get your _app secret_ and _app key_.

While setting you app there you should add `http://localhost:8000/` `http://localhost:8000/app/` and `http://localhost:8000/oauth/login/facebook/` as _valid OAuth redirect URIs_ (it's inside _Settings_, _Advanced_).

### Settings

Copy `contrib/.env.sample` as `.env` in the project's root folder and adjust your settings.

At this point it's crucial to configure the acceess to you database ([PostgreSQL](http://www.postgresql.org) is not required, but recommended), and to add the _app secret_ and _key_ you got during the previous step.


### Migrations

Once you're done with requirements, dependencies and settings, create the basic structure at the database and create a super-user for you:

```
python manage.py migrate
python manage.py createsuperuser
```

### In case you are turning off the _debug mode_

If you are going to run the app with `DEBUG=False` first you will have to set the stage for your static files: 

```
python manage.py collectstatic
```

### Ready?

Not sure? Run `python manage.py check` and `python manage.py test` just in case.

### Accessing Valentina

Run the server with `python manage.py runserver` and load [localhost:8000](http://localhost:8000) with your favorite browser.

If you want to test the _login required_ area, as a developer you can login through [Django Admin](http://localhost:8000/admin/) and then go back to the [root](http://localhost:8000/).

## Thanks

Thanks to [Golden Roof](https://thenounproject.com/term/settings/134561), [ChangHoon](https://thenounproject.com/term/log-out/76004/), [João Proença](https://thenounproject.com/term/search/123746/) and [Sergey Demushkin](https://thenounproject.com/term/report/135792/) for their beautiful icons.

##I License

Licensed under the [MIT License](LICENSE).