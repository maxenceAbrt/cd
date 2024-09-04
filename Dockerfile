# Stage 1: Build the Python application
FROM python:latest AS builder

# Set the working directory in the container
WORKDIR /app

# Copy the Python application source code into the container
COPY . .

# Install any required Python packages (none in this case, but this is where you'd do it)
# RUN pip install -r requirements.txt

# Stage 2: Create a minimal scratch-like container
FROM python:3.12-slim

# Copy the source code from the builder stage
COPY --from=builder /app /app

# Set the working directory to /app
WORKDIR /app

# Expose port 3000 which the application listens on
EXPOSE 3000

# Set environment variables if necessary (e.g., FILE_PATH and GREETING)
# ENV FILE_PATH=/custom/path
# ENV GREETING=HelloCustom

# Run the Python application
CMD ["python", "app.py"]
