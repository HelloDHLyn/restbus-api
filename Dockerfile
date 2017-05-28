FROM vapor/vapor:latest

# Install requirements
RUN apt-get install cmysql libxml2-dev -y

# Add application
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD . /usr/src/app

# Build Project
RUN vapor build