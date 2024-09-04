FROM python:3.9

WORKDIR /app

COPY requirements-service.txt requirements-service.txt
RUN pip install -r requirements-service.txt

COPY . .
COPY my_collection.json /app/ 
COPY my_collection_video.json /app/ 

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8991"]
