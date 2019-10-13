# django-vue

Django Vue scaffold. Runs with docker-compose. Requires nginx so that the vue.js front end can leverage cookie based auth within Django.

## Running

### Docker
#### Start
```docker-compose up```

Nativate to `localhost:8000` to view api
Nativate to `localhost:8080` to view client

To run Tests:
```bash
make test
```
#### Stop (clears the db)
```bash
$ docker-compose down -v
```
Or shorthand:
```bash
$ make stop
```
### Locally
1. Start Postgres
```bash
make dbstart
```
2. Start Cient in new terminal
```
$ cd client
$ npm run serve
```

Run tests with:
```bash
npm run unit
```

3. Run migrations (if needed), Start API in new terminal
```bash
$ cd backend
$  pip install -r requirements.txt
$ ./manage.py migrate 
$ ./manage.py runserver
```

Run tests with:
```bash
$ tox
```

Nativate to `localhost:8000` to view api


