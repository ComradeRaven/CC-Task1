# Python basement
FROM python:3.11

# Application directory
WORKDIR /app

# Copy script
COPY ./app.py ./
# Copy html
COPY ./templates/ ./templates/

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Install python requirements
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Connect to database
EXPOSE 5000

# Run program
CMD ["flask", "run"]