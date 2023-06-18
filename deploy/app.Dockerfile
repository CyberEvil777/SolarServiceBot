FROM python:3.9-slim

ENV PROJECT_ROOT /project
ENV SRC_DIR /src
ENV DEPLOY_DIR ./deploy

RUN mkdir $PROJECT_ROOT
COPY $SRC_DIR/gunicorn.conf.py $PROJECT_ROOT
COPY $DEPLOY_DIR/run_django.sh $PROJECT_ROOT


RUN apt-get update && \
    apt-get install -f -y postgresql-client-common postgresql-client libpq-dev && \
    rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man && \
    apt-get clean

RUN pip install --upgrade pip wheel pipenv

COPY ./Pipfile $PROJECT_ROOT
COPY ./Pipfile.lock $PROJECT_ROOT

WORKDIR $PROJECT_ROOT
RUN pipenv install --deploy --system --dev

COPY ./$SRC_DIR $PROJECT_ROOT

RUN chmod +x $PROJECT_ROOT/run_django.sh
CMD ["./run_django.sh"]
