# Use an official Python runtime as a parent image
FROM python:3.6

RUN mkdir /app
COPY . /app
WORKDIR /app

# Make port 8080 available to the world outside this container
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
EXPOSE 8080

ENTRYPOINT ["sh","/app/entrypoint.sh"]