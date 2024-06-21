FROM python:3.10.3-slim-buster

# stream output to console
ENV PYTHONUNBUFFERED=1

# install poetry inside the container
RUN pip install poetry==1.8.2

WORKDIR /app

# add /app/src to PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/app/src"

# copy the pyproject.toml and poetry.lock files into the container
COPY pyproject.toml poetry.lock /app/

# install Python dependencies from the pyproject.toml file
RUN poetry install

# copy all the source code into the container
# COPY src/*.py /app/src/
COPY . /app/

CMD ["poetry", "run", "python", "src/main.py"]