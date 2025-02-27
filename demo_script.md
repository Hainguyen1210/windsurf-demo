# Windsurf Demo Script

This script provides a step-by-step guide for demonstrating Windsurf's capabilities. Follow this script to showcase how Windsurf can help build a complete application from scratch.

## Demo Preparation

1. Install Windsurf on your machine
2. Clone the windsurf-demo repository:
   ```bash
   git clone git@github.com:Hainguyen1210/windsurf-demo.git
   cd windsurf-demo
   ```
3. Run the initialization script to create a new project:
   ```bash
   ./init.sh task-manager my-demo
   ```
4. Open the task-manager project in Windsurf

## Demo Script

### 1. Introduction (2 minutes)

"Today I'm going to show you how Windsurf, an agentic IDE, can help us build a complete application with minimal effort. We'll build a task management application with a Go backend, React frontend, and Docker deployment."

### 2. Building the Backend API (5 minutes)

1. Open the main.go file in the backend directory
2. Show the minimal starter template
3. Prompt Windsurf:
   ```
   Expand this minimal Go/Gin application into a complete task management API with the following features:
   1. A Task model with fields for ID, title, description, status, due date, and timestamps
   2. SQLite database integration using GORM
   3. CRUD endpoints for tasks
   4. Proper error handling and validation
   5. Middleware for logging and CORS
   ```
4. Review the generated code with the audience, highlighting:
   - The model definitions
   - Database setup
   - API endpoint implementations
   - Error handling

### 3. Testing the API (2 minutes)

1. Navigate to the backend directory in the terminal
2. Run the application:
   ```bash
   go run main.go
   ```
3. Test the API using curl or Postman:
   ```bash
   # Create a task
   curl -X POST http://localhost:8080/api/tasks -H "Content-Type: application/json" -d '{"title":"Demo Task","description":"Testing Windsurf","status":"pending","due_date":"2025-03-01T00:00:00Z"}'
   
   # Get all tasks
   curl http://localhost:8080/api/tasks
   ```

### 4. Building the Frontend (5 minutes)

1. Open the App.tsx file in the frontend directory
2. Show the minimal starter template
3. Prompt Windsurf:
   ```
   Expand this minimal React application into a complete task management frontend with the following features:
   1. Components for displaying, creating, updating, and deleting tasks
   2. Connection to our Go API using Axios
   3. Clean, responsive design with CSS
   4. Proper error handling and loading states
   5. TypeScript interfaces for type safety
   ```
4. Review the generated code with the audience, highlighting:
   - Component structure
   - API integration
   - UI design
   - TypeScript types

### 5. Dockerizing the Application (3 minutes)

1. Open the docker-compose.yml file
2. Show the minimal starter template
3. Prompt Windsurf:
   ```
   Create Dockerfiles for both the backend and frontend applications, and update the docker-compose.yml file to run the complete application. Include:
   1. Multi-stage build for the Go backend
   2. Nginx configuration for the React frontend
   3. Proper networking between containers
   4. Volume mounting for the SQLite database
   ```
4. Review the generated Docker configuration with the audience

### 6. Running the Complete Application (2 minutes)

1. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```
2. Navigate to http://localhost:3000 in a browser
3. Demonstrate the working application by creating, viewing, updating, and deleting tasks

### 7. Conclusion (1 minute)

"As you've seen, Windsurf has helped us build a complete application with minimal effort. We've created a backend API, frontend client, and Docker deployment in just a few minutes. This demonstrates how Windsurf can accelerate development and help developers focus on solving problems rather than writing boilerplate code."

## Additional Demo Options

If you have more time, consider demonstrating:

1. **Adding Authentication**: Prompt Windsurf to add JWT authentication
2. **Implementing Testing**: Prompt Windsurf to add unit and integration tests
3. **Setting up CI/CD**: Prompt Windsurf to create a GitHub Actions workflow
4. **Adding Advanced Features**: Prompt Windsurf to add features like task categories, priorities, or notifications
