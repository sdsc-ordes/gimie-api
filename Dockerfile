FROM python:3.9
RUN pip3 install 'fastapi==0.95.2' 'uvicorn==0.22.0'
RUN pip3 install 'gimie==0.4.0'
COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "15400"]
