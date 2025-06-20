FROM python:3.13.3-slim


ENV PYTHONUNBUFFERED=1 
ENV PORT=8080 

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE $PORT

CMD ["python", "main.py"]
