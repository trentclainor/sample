FROM python:3.6.2

ENV PYTHONUNBUFFERED 1

RUN apt-get -qq update
RUN apt-get -yqq install gettext-base

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements

RUN pip install --upgrade pip
RUN pip install -r /requirements/production.txt \
    && groupadd -r django \
    && useradd -r -g django django


COPY . /app
RUN chown -R django /app

COPY ./compose/celery/beat.sh /beat.sh
COPY ./compose/celery/worker.sh /worker.sh
COPY ./compose/celery/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh \
    && sed -i 's/\r//' /beat.sh \
    && sed -i 's/\r//' /worker.sh \
    && chmod +x /entrypoint.sh \
    && chown django /entrypoint.sh \
    && chmod +x /beat.sh \
    && chown django /beat.sh \
    && chmod +x /worker.sh \
    && chown django /worker.sh

RUN mkdir /app/staticfiles
RUN chown -R django /app/staticfiles

RUN mkdir /app/media
RUN chown -R django /app/media

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
