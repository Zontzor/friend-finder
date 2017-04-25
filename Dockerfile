FROM python:3.4

MAINTAINER Alex Kiernan

# Update OS
RUN apt-get -y update
RUN apt-get -y upgrade

# Install geospatial package
RUN apt-get -y install libgdal-dev

# Create app directory
COPY . /app
WORKDIR /app

RUN mkdir -p /var/log/django

# Update pip and install reqs
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose listening port
EXPOSE 8000

# Run server
ENTRYPOINT ["python"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
