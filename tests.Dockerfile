FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/home/app

RUN mkdir -p $APP_HOME \
    && addgroup -S app \
    && adduser -S app -G app \
    && apk update \
    && apk add libpq

RUN pip install --upgrade pip
COPY ./requirements-dev.txt .
RUN pip install -r requirements-dev.txt

COPY --from=ghcr.io/ufoscout/docker-compose-wait:latest /wait /wait

WORKDIR $APP_HOME

COPY . .

RUN chown -R app:app .
USER app

CMD /wait && pytest -v -s --disable-warnings
