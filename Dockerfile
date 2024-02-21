FROM python:3.9

RUN pip3 install 'fastapi~=0.109.2' 'uvicorn~=0.27.0.post1'
RUN pip3 install 'gimie~=0.6.1'

COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "15400"]
