FROM python:3.12-slim

# Use /app as the working directory inside the container.
WORKDIR /app

# Prevent Python from writing __pycache__ files and keep logs visible immediately.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy requirements first so Docker can cache dependency installation.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container.
COPY . .

# Run the ETL pipeline as a Python package.
CMD ["python", "-m", "src.main"]