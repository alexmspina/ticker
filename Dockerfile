FROM python:3.9.2-buster as base-env
RUN apt-get update && apt-get -y install postgresql-client
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.0.10 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM base-env as build-env
RUN pip install poetry

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev

FROM base-env
ENV FLASK_ENV=production
ENV TICKER_CONFIG_FILE=dev_config.toml
COPY --from=build-env $PYSETUP_PATH $PYSETUP_PATH
COPY . /app/
WORKDIR /app
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--timeout", "120", "--workers", "4", "--threads", "4", "ticker:create_app()"]