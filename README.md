# flask_frontend
flask_frontend is a flask application, that serve data from [flask_backend](https://github.com/BorodaUA/flask_backend) as frontend flask app. And it is part of the [webportal](https://github.com/BorodaUA/webportal) project.

## How to use:
### Local development mode:
1. Clone the repo
2. Create .env file inside the repo with following data:
    - SECRET_KEY=string for flask app secret key
    - JWT_SECRET_KEY=string for Flask-JWT-Extended library secret key
    - BACKEND_SERVICE_NAME=name of the flask_backend service from the [webportal](https://github.com/BorodaUA/webportal) docker-compose.yml
    - BACKEND_SERVICE_PORT=number of port flask_backend service from the [webportal](https://github.com/BorodaUA/webportal) docker-compose.yml
3. cd to the folder /usr/src/flask_frontend/ and run command: "python `run.py`"