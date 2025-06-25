FROM python:3.13.3-alpine
ENV PYTHONUNBUFFERED=1 
ENV PORT=8080 
WORKDIR /app
RUN mkdir /app/data && chmod a+rwx /app/data
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE $PORT
CMD ["python", "main.py"]
