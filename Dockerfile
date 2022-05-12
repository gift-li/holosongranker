FROM python:3.9-slim-buster

WORKDIR /web
COPY . .

RUN pip install pipenv \
    pipenv install --dev \
    pipenv shell \
    python make makemigrations \
    python migrate

CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]