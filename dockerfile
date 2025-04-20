# Use official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Fix IPv6 preference issue (force IPv4)
RUN echo 'precedence ::ffff:0:0/96  100' >> /etc/gai.conf

# Install dependencies
COPY requirements.txt .
RUN apt update && apt install -y curl && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . .

# Run the Django dev server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]