FROM python:3.9
RUN pip3 install fastapi uvicorn
#RUN pip3 install gimie
RUN pip install git+https://github.com/SDSC-ORD/gimie.git@0.6.0
COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "15400"]