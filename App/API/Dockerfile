FROM python:3.7-alpine
LABEL key="GagandeepSingh"

ENV PYTHONUNBUFFERED 1

RUN pip install Flask Flask-PyMongo dnspython
RUN apk add --no-cache bash

RUN mkdir /api
WORKDIR /api
COPY ./api /api

RUN adduser -D user
USER user

ENTRYPOINT [ "python" ]
CMD [ "api.py" ]