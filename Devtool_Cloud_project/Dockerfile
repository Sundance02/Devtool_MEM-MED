# Base image
FROM python:3.10-slim

# Install PostgreSQL development libraries and other dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Set up static files
RUN python manage.py collectstatic --no-input

# Expose port
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
