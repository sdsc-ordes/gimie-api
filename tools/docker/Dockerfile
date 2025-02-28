FROM python:3.9

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt


COPY ./app /app
WORKDIR /

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "15400"]
