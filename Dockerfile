FROM python:3.7-alpine

# Update installation utility
RUN apk update
RUN apk upgrade

# Environment variables
ENV TZ UTC

# Create working directory
RUN mkdir /app
WORKDIR /app

# Install the requirements
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Run the server on container startup
CMD [ "python", "-u","WebServer.py"]