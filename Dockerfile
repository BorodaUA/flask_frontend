FROM python:3.8.3-alpine
#
RUN mkdir /usr/src/flask_frontend/
WORKDIR /usr/src/flask_frontend/
#
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
#
RUN apk update
RUN apk add --no-cache \
    python3-dev \
    postgresql-dev \
    gcc \
    musl-dev \
    libxml2-dev \
    libxslt-dev \
    git
COPY . /usr/src/flask_frontend/
RUN pip install -r requirements.txt
#
ENTRYPOINT ["sh", "entrypoint.sh"]
