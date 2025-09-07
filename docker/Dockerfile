# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy backend code into container
COPY ../backend /app/backend
COPY ../requirements.txt /app/requirements.txt
COPY ../.env /app/.env

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for FastAPI
EXPOSE 8000

# Command to run FastAPI with Uvicorn
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
