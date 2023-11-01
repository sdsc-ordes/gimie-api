FROM python:3.9
RUN pip install fastapi uvicorn
RUN pip install gimie==0.6.1
COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "15400"]
