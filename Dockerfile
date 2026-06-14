# Base image
FROM python:3.10

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8000

# Run using Gunicorn (recommended)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "A_sys.wsgi:application"]