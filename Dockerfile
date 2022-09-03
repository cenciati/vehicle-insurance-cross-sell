FROM python:3.10-slim

WORKDIR /src/api

COPY ./src/api .
COPY ./requirements.txt .

RUN apt-get update && \
    apt-get install -y
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "-m", "handler.py"]