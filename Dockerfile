FROM python:3.10.6-slim

WORKDIR /service

COPY ./src ./src
COPY ./models ./models
COPY ./requirements.txt .

RUN apt-get update && \
    apt-get install -y
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8000

CMD ["python3", "-m", "src.api.handler"]