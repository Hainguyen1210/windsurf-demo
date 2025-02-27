# Windsurf Prompt Guide

This guide provides example prompts to help you build a complete application using Windsurf, from API development to frontend creation, dockerization, and test automation.

## Getting Started

1. Clone this repository
2. Create your own branch
3. Open the project in Windsurf
4. Use the prompts below as inspiration

## Building a Complete Application with Windsurf

### Step 1: Create a Backend API

```
Create a Go API with Gin framework for a task management application. The API should:
1. Have a Task model with fields for ID, title, description, status, due date, and timestamps
2. Use GORM with SQLite for data persistence
3. Implement CRUD endpoints for tasks
4. Include proper error handling and validation
5. Use middleware for logging and CORS
```

### Step 2: Build a Frontend Client

```
Create a React frontend with TypeScript for the task management API. The frontend should:
1. Have components for displaying, creating, updating, and deleting tasks
2. Connect to the Go API using Axios
3. Include proper error handling and loading states
4. Have a clean, responsive design
5. Use TypeScript for type safety
```

### Step 3: Dockerize the Application

```
Dockerize the task management application with:
1. A multi-stage Dockerfile for the Go backend
2. A Dockerfile for the React frontend using Nginx
3. A docker-compose.yml file to run both services together
4. Volume mounting for the SQLite database
5. Proper networking between containers
```

### Step 4: Implement Test Automation

```
Create comprehensive tests for the task management application:
1. Complete the Selenium test template in the testing/selenium directory
2. Implement the missing update and delete task tests
3. Add tests for form validation and error handling
4. Set up the test environment to run in the CI/CD pipeline
5. Generate test reports for easy analysis
```

## Example Project Structure

```
project/
├── backend/              # Go API
├── frontend/             # React frontend
├── testing/              # Test automation
│   └── selenium/         # Selenium tests
├── docker-compose.yml    # Docker composition
└── .github/workflows/    # CI configuration
```

## Tips for Effective Prompting

1. **Be specific**: Clearly describe what you want to build
2. **Provide context**: Explain how components should work together
3. **Ask for explanations**: Request that Windsurf explain its implementation choices
4. **Iterate**: Start simple and add complexity in subsequent prompts
5. **Request improvements**: Ask Windsurf to optimize or refactor code

## Sample Workflow

1. Start by creating the backend API
2. Test the API endpoints using curl or Postman
3. Create the frontend to connect with the API
4. Dockerize both components
5. Implement tests for all components
6. Set up CI/CD pipeline

## Advanced Prompts

### Adding Authentication

```
Add JWT authentication to the task management application:
1. Implement user registration and login endpoints in the API
2. Create middleware to verify JWT tokens
3. Add login and registration forms to the frontend
4. Secure API endpoints to require authentication
5. Store tokens securely in the frontend
```

### Implementing Advanced Features

```
Add the following features to the task management application:
1. Task categories or tags
2. Task priority levels
3. Due date notifications
4. Task assignment to users
5. Task comments or activity history
```

### Optimizing Performance

```
Optimize the performance of the task management application:
1. Implement caching for API responses
2. Add pagination for task listings
3. Optimize React rendering with memoization
4. Implement database indexing
5. Add load testing and performance monitoring
```

### Enhancing Test Automation

```
Enhance the Selenium test suite for the task management application:
1. Add data-driven testing for different task scenarios
2. Implement page object pattern for better test organization
3. Add visual regression testing
4. Set up parallel test execution for faster feedback
5. Implement test retries for flaky tests
```

Remember that Windsurf works best when you provide clear, specific instructions. Start with a high-level description and then refine with more detailed prompts as needed.
