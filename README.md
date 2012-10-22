# Telostats

## Requirements:

- `pip install -r requirements.txt`
- `gem install sass bourbon`
- `npm install -g coffee-script` (might require sudo)

## Dev

- `cd telostats`
- `mkvirtualenv telostats`
- `pip install -r requirements.txt`
- `pip install -r requirements.txt`
- `gem install sass bourbon`
- `npm install -g coffee-script` (might require sudo)
- `createdb telostats`
- Create `.env` file (and use https://github.com/kennethreitz/autoenv) with required env vars:`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `DJANGO_SECRET_KEY`, `TEMPODB_KEY`, `TEMPODB_SECRET`


## Running in development

Don't start separate processes for sass/coffee/runserver. Just do:

    foreman start -f Procfile.dev


## Random Useful Info

Tel Aviv Bounding Box [lon, lat]:
* Top-Left: [34.7422646, 32.1460661]
* Bottom-Right: [34.8511153, 32.0294328]