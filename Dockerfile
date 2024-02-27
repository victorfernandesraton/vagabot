# Dockerfile
FROM python:3.11-slim-bookworm

# Poetry install
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
RUN pip install poetry

# Set the working directory in the container
WORKDIR /usr/app

# Install dependencies
COPY pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY ./vagabot/ ./vagabot/
COPY script.py ./

RUN ls -la

# Set the entrypoint to run your script
ENTRYPOINT ["python", "script.py"]
