FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

ENV PYTHONPATH "${PYTHONPATH}:/"
# ENV PORT=8000

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-root --no-dev

COPY ./app /app

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku			
CMD gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT main:app
