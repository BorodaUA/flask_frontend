FROM python:3.8.3-alpine
RUN mkdir /usr/src/front_1/
WORKDIR /usr/src/front_1/
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev && \ 
    apk add libxml2-dev && apk add libxslt-dev && apk add python3-dev
COPY . /usr/src/front_1/
RUN pip install -r requirements.txt
CMD [ "python", "run.py" ]