# Use the official lightweight Python image.
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

# Expose the port Flask runs on
EXPOSE 8080

# Set environment variable for Flask
ENV PORT 8080

# Start Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"] 