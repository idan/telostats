# Telostats

## Dev

```bash
$ cd telostats
$ mkvirtualenv telostats
$ pip install -r requirements.txt
$ gem install sass bourbon
$ npm install -g coffee-script  # might require sudo
$ createdb telostats
```

Create `.env` file (and use [https://github.com/kennethreitz/autoenv](https://github.com/kennethreitz/autoenv)) with required env vars:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `DJANGO_SECRET_KEY`
  - `TEMPODB_KEY`
  - `TEMPODB_SECRET`

Don't start separate processes for sass/coffee/runserver. Just do:

    foreman start -f Procfile.dev

## Copyright

Copyright (c) 2012 Idan Gazit, Yuval Adam, and Contributors

See `LICENSE.txt` for more info.
