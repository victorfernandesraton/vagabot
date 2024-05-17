# Dockerfile
FROM python:3.11-slim-bookworm

# Set the working directory in the container
WORKDIR /usr/app

# Poetry install
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Install dependencies
COPY pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY ./vagabot/ ./vagabot/

COPY script.py ./

# Set the entrypoint to run your script
ENTRYPOINT ["python", "script.py"]
