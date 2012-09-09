Tel-O-Stats
===========

Dev
---

 1. `cd telostats`
 2. `mkvirtualenv telostats`
 3. `pip install -r requirements.txt`
 4. `createdb telostats`
 5. Create `.env` file (and use https://github.com/kennethreitz/autoenv) with required env vars:`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `DJANGO_SECRET_KEY`, `TEMPODB_KEY`, `TEMPODB_SECRET`


Random Useful Info
------------------

Tel Aviv Bounding Box [lon, lat]:
* Top-Left: [34.7422646, 32.1460661]
* Bottom-Right: [34.8511153, 32.0294328]