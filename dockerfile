# Use the official lightweight Python image as the base
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8000

# Set environment variables for production settings
ENV PYTHONUNBUFFERED=1
ENV APP_MODULE=app.main:app

# Run FastAPI using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
