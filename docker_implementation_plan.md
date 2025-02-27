# Docker Implementation Plan

This plan outlines the steps to containerize both the Go backend API and React frontend application, and to set up a Docker Compose configuration for running the entire stack.

## Backend Dockerfile

```dockerfile
# Stage 1: Build the Go application
FROM golang:1.16-alpine AS builder

# Install required dependencies for CGO (SQLite)
RUN apk add --no-cache gcc musl-dev

WORKDIR /app

# Copy go mod and sum files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY . .

# Build the application
RUN CGO_ENABLED=1 GOOS=linux go build -a -o api ./cmd/api

# Stage 2: Create the final image
FROM alpine:latest

# Install required runtime dependencies
RUN apk --no-cache add ca-certificates

WORKDIR /app

# Copy the binary from builder
COPY --from=builder /app/api .

# Create directory for SQLite database
RUN mkdir -p /app/data

# Set environment variables
ENV GIN_MODE=release
ENV DB_PATH=/app/data/tasks.db

# Expose port
EXPOSE 8080

# Run the application
CMD ["./api"]
```

## Frontend Dockerfile

```dockerfile
# Stage 1: Build the React application
FROM node:14-alpine as build

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy all files
COPY . .

# Set the API URL for production
ENV REACT_APP_API_URL=http://localhost:8080/api/v1

# Build the application
RUN npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:alpine

# Copy the build output to replace the default nginx contents
COPY --from=build /app/build /usr/share/nginx/html

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
```

## Nginx Configuration for Frontend

```nginx
# nginx.conf
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Serve static files
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Proxy API requests to the backend
    location /api/ {
        proxy_pass http://backend:8080/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## Docker Compose Configuration

```yaml
version: '3'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: task-manager-api
    ports:
      - "8080:8080"
    environment:
      - GIN_MODE=release
      - DB_PATH=/app/data/tasks.db
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    networks:
      - task-manager-network

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: task-manager-ui
    ports:
      - "3000:80"
    depends_on:
      - backend
    restart: unless-stopped
    networks:
      - task-manager-network

networks:
  task-manager-network:
    driver: bridge
```

## Implementation Steps

### 1. Create Backend Dockerfile

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create the Dockerfile:
   ```bash
   touch Dockerfile
   ```

3. Copy the backend Dockerfile content into the file.

### 2. Create Frontend Dockerfile and Nginx Configuration

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Create the Dockerfile:
   ```bash
   touch Dockerfile
   ```

3. Copy the frontend Dockerfile content into the file.

4. Create the Nginx configuration:
   ```bash
   touch nginx.conf
   ```

5. Copy the Nginx configuration content into the file.

### 3. Create Docker Compose Configuration

1. Navigate to the project root:
   ```bash
   cd ..
   ```

2. Create the docker-compose.yml file:
   ```bash
   touch docker-compose.yml
   ```

3. Copy the Docker Compose configuration content into the file.

4. Create a data directory for the SQLite database:
   ```bash
   mkdir -p data
   ```

### 4. Build and Run with Docker Compose

1. Build the images:
   ```bash
   docker-compose build
   ```

2. Start the containers:
   ```bash
   docker-compose up -d
   ```

3. Check the logs:
   ```bash
   docker-compose logs -f
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8080/api/v1/tasks

### 5. Stop the Containers

```bash
docker-compose down
```

## Docker Best Practices

1. **Multi-stage builds**: Used to minimize image size by separating build and runtime environments.
2. **Specific base images**: Used specific versions of base images to ensure consistency.
3. **Layer caching**: Organized Dockerfiles to take advantage of Docker's layer caching mechanism.
4. **Environment variables**: Used environment variables for configuration.
5. **Volume mounting**: Used volumes to persist data outside of containers.
6. **Health checks**: Can be added to ensure services are running correctly.
7. **Network isolation**: Used a dedicated network for communication between services.

## Additional Docker Features to Consider

1. **Docker Secrets**: For managing sensitive information like API keys.
2. **Docker Healthchecks**: To ensure services are running correctly.
3. **Docker Compose Profiles**: To run different service combinations.
4. **Docker Compose Environment Files**: To manage environment variables.

## Production Considerations

1. **Container Orchestration**: Consider using Kubernetes for production deployments.
2. **Database**: Replace SQLite with a more robust database like PostgreSQL.
3. **Logging**: Implement centralized logging with ELK stack or similar.
4. **Monitoring**: Add Prometheus and Grafana for monitoring.
5. **CI/CD**: Integrate with CI/CD pipelines for automated builds and deployments.
