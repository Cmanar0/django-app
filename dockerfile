FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install curl + dependencies and set IPv4 preference
RUN apt update && apt install -y curl && \
    echo 'precedence ::ffff:0:0/96  100' >> /etc/gai.conf

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
