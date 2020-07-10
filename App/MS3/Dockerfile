FROM python:3.7-alpine
LABEL key="GagandeepSingh"

ENV PYTHONUNBUFFERED 1

RUN pip install Flask Flask-PyMongo dnspython requests
RUN apk add --no-cache bash

RUN mkdir /orders
WORKDIR /orders
COPY ./orders /orders

RUN adduser -D user
USER user

ENTRYPOINT [ "python" ]
CMD [ "orders.py" ]