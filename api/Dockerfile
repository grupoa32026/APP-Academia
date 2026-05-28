FROM python:3.8.18
RUN mkdir /app
WORKDIR /app
ADD ./web .
RUN pip install -r requirements.txt
RUN mkdir -p /app/logs
EXPOSE 8080
CMD ["python", "app.py"]
