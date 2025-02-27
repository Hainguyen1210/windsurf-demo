# Detailed Windsurf Demo Script

## Introduction (2 minutes)
- Welcome and introduce Windsurf as an agentic IDE
- Explain the demo's purpose: to showcase Windsurf's ability to help write code, build APIs, create frontends, dockerize applications, and implement test automation
- Outline the application we'll build: a Task Manager with Go/Gin backend and React frontend

## Part 1: Backend API Development with Go/Gin (10 minutes)

### 1.1 Project Setup (2 minutes)
- Create project structure
- Initialize Go module
- Add Gin and GORM dependencies
- Explain the project organization

### 1.2 Data Models (2 minutes)
- Define Task model with GORM
- Add validation tags
- Implement database connection

### 1.3 API Endpoints (3 minutes)
- Create router setup
- Implement CRUD endpoints:
  - GET /api/v1/tasks (list all tasks)
  - GET /api/v1/tasks/:id (get task by ID)
  - POST /api/v1/tasks (create new task)
  - PUT /api/v1/tasks/:id (update task)
  - DELETE /api/v1/tasks/:id (delete task)
- Add middleware for logging, error handling, and CORS

### 1.4 Testing the API (3 minutes)
- Write unit tests for handlers
- Demonstrate API functionality using curl or Postman
- Show how Windsurf helps with test generation

## Part 2: Frontend Development with React (8 minutes)

### 2.1 Project Setup (2 minutes)
- Create React application with TypeScript
- Add required dependencies
- Set up project structure

### 2.2 Components (3 minutes)
- Create TaskList component
- Create TaskForm component
- Create TaskItem component
- Implement state management

### 2.3 API Integration (3 minutes)
- Create API service
- Connect components to API
- Handle loading states and errors

## Part 3: Dockerization (5 minutes)

### 3.1 Backend Dockerfile (2 minutes)
- Create multi-stage Dockerfile for Go application
- Explain the build process
- Show optimization techniques

### 3.2 Frontend Dockerfile (1 minute)
- Create Dockerfile for React application
- Explain build and serve process

### 3.3 Docker Compose (2 minutes)
- Create docker-compose.yml
- Configure services and networking
- Demonstrate running the application with docker-compose

## Part 4: Test Automation (5 minutes)

### 4.1 Backend Tests (2 minutes)
- Show unit tests for Go API
- Demonstrate integration tests
- Explain test coverage

### 4.2 Frontend Tests (2 minutes)
- Show component tests
- Demonstrate integration tests with React Testing Library
- Explain mocking API calls

### 4.3 CI Pipeline (1 minute)
- Show GitHub Actions or similar CI configuration
- Explain automated testing and deployment process

## Conclusion (2 minutes)
- Recap what we've built and demonstrated
- Highlight Windsurf's capabilities in helping with the development process
- Q&A

## Demo Code Snippets

### Go API Main File
```go
package main

import (
    "log"
    
    "github.com/gin-gonic/gin"
    "github.com/yourusername/windsurf-demo/internal/database"
    "github.com/yourusername/windsurf-demo/internal/handlers"
    "github.com/yourusername/windsurf-demo/internal/middleware"
)

func main() {
    // Initialize database
    db, err := database.InitDB()
    if err != nil {
        log.Fatalf("Failed to connect to database: %v", err)
    }
    
    // Set up Gin router
    r := gin.Default()
    
    // Add middleware
    r.Use(middleware.Logger())
    r.Use(middleware.CORS())
    
    // Register routes
    api := r.Group("/api/v1")
    {
        tasks := api.Group("/tasks")
        {
            taskHandler := handlers.NewTaskHandler(db)
            tasks.GET("", taskHandler.ListTasks)
            tasks.GET("/:id", taskHandler.GetTask)
            tasks.POST("", taskHandler.CreateTask)
            tasks.PUT("/:id", taskHandler.UpdateTask)
            tasks.DELETE("/:id", taskHandler.DeleteTask)
        }
    }
    
    // Start server
    r.Run(":8080")
}
```

### React Component Example
```tsx
import React, { useState, useEffect } from 'react';
import { fetchTasks, createTask, updateTask, deleteTask } from '../services/api';
import TaskForm from './TaskForm';
import TaskItem from './TaskItem';

const TaskList: React.FC = () => {
    const [tasks, setTasks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    
    useEffect(() => {
        loadTasks();
    }, []);
    
    const loadTasks = async () => {
        try {
            setLoading(true);
            const data = await fetchTasks();
            setTasks(data);
            setError('');
        } catch (err) {
            setError('Failed to load tasks');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };
    
    const handleCreateTask = async (task) => {
        try {
            await createTask(task);
            loadTasks();
        } catch (err) {
            setError('Failed to create task');
            console.error(err);
        }
    };
    
    // Additional handlers for update and delete...
    
    return (
        <div className="task-list">
            <h2>Tasks</h2>
            {error && <div className="error">{error}</div>}
            <TaskForm onSubmit={handleCreateTask} />
            {loading ? (
                <p>Loading tasks...</p>
            ) : (
                <div>
                    {tasks.length === 0 ? (
                        <p>No tasks found</p>
                    ) : (
                        tasks.map(task => (
                            <TaskItem 
                                key={task.id} 
                                task={task}
                                onUpdate={(updatedTask) => handleUpdateTask(task.id, updatedTask)}
                                onDelete={() => handleDeleteTask(task.id)}
                            />
                        ))
                    )}
                </div>
            )}
        </div>
    );
};

export default TaskList;
```

### Docker Compose Example
```yaml
version: '3'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      - GIN_MODE=release
      - DB_PATH=/app/data/tasks.db
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend
    restart: unless-stopped
```
