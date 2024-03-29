FROM python:3.8-alpine

WORKDIR /app

ENV POETRY_VERSION=1.3.2

RUN apk update
RUN apk add --no-cache gcc libffi-dev musl-dev postgresql-dev

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000"]