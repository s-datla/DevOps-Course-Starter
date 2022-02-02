FROM python:3.9.7 as baseImage

EXPOSE 8000

# Get Poetry
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
RUN pip install poetry

# Copy code and install poetry dependencies
WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false \
    && poetry install
COPY . /app

FROM baseImage as production

# Run gunicorn for production 
ENTRYPOINT [ "poetry", "run", "gunicorn", "--config", "gunicorn.conf.py", "todo_app.app:create_app()" ]

FROM baseImage as development

# Run flask for development 
ENTRYPOINT [ "poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=8000"]
