FROM python:3.9
RUN pip3 install fastapi uvicorn
RUN pip3 install gimie
COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "15400"]
RUN export ACCESS_TOKEN=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