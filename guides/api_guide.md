# Building APIs with Go and Gin

This guide will help you use Windsurf to build a RESTful API using Go and the Gin framework.

## Overview

Go is a statically typed, compiled language known for its simplicity and performance. Gin is a web framework written in Go that features a martini-like API with much better performance.

## Getting Started with Windsurf

Here's how to use Windsurf to create your Go/Gin API:

1. Open your project in Windsurf
2. Use the following prompts to get started

## Sample Prompts for Windsurf

### Setting Up the Project

```
Create a new Go API project with Gin framework. Set up the basic project structure with:
- A cmd/api directory for the entry point
- An internal directory with packages for handlers, models, database, and middleware
- A tests directory for unit and integration tests
```

### Creating Models

```
Create a Task model in Go with the following fields:
- ID (uint)
- Title (string, required)
- Description (string)
- Status (string, with default value "pending")
- DueDate (time.Time, optional)
- CreatedAt and UpdatedAt timestamps
```

### Setting Up Database Connection

```
Create a database connection module using GORM with SQLite. Implement functions to:
- Initialize the database connection
- Auto-migrate the Task model
- Provide a method to get the database instance
```

### Implementing API Handlers

```
Create a TaskHandler struct with methods for:
- ListTasks (GET /tasks)
- GetTask (GET /tasks/:id)
- CreateTask (POST /tasks)
- UpdateTask (PUT /tasks/:id)
- DeleteTask (DELETE /tasks/:id)

Each handler should use the database connection to perform CRUD operations.
```

### Setting Up Middleware

```
Create middleware for:
- CORS support
- Request logging
- Error handling
```

### Creating the Main Application

```
Create the main.go file that:
- Initializes the database
- Sets up the Gin router
- Registers middleware
- Defines API routes
- Starts the HTTP server
```

### Writing Tests

```
Write unit tests for the Task handlers covering:
- Creating a task
- Getting a task by ID
- Listing all tasks
- Updating a task
- Deleting a task
```

## Project Structure

A typical Go/Gin API project structure looks like this:

```
backend/
├── cmd/
│   └── api/
│       └── main.go           # Entry point for the application
├── internal/
│   ├── database/
│   │   └── db.go             # Database connection and initialization
│   ├── handlers/
│   │   └── task_handler.go   # HTTP handlers for task endpoints
│   ├── middleware/
│   │   ├── cors.go           # CORS middleware
│   │   └── logger.go         # Logging middleware
│   └── models/
│       └── task.go           # Task data model
├── tests/
│   └── handlers_test.go      # Tests for HTTP handlers
├── Dockerfile                # Docker configuration
└── go.mod                    # Go module file
```

## API Endpoints

A typical RESTful API for a task manager might include:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/tasks | List all tasks |
| GET | /api/v1/tasks/:id | Get task by ID |
| POST | /api/v1/tasks | Create new task |
| PUT | /api/v1/tasks/:id | Update task |
| DELETE | /api/v1/tasks/:id | Delete task |

## Best Practices

1. **Use proper error handling**: Return appropriate HTTP status codes and error messages
2. **Validate input data**: Use struct tags or middleware for validation
3. **Use dependency injection**: Pass dependencies like the database connection to handlers
4. **Write tests**: Cover all API endpoints with tests
5. **Use middleware for cross-cutting concerns**: Logging, authentication, CORS, etc.
6. **Document your API**: Use comments or tools like Swagger

## Example Code Snippets

### Task Model

```go
// internal/models/task.go
package models

import (
    "time"
    
    "gorm.io/gorm"
)

type Task struct {
    ID          uint      `json:"id" gorm:"primaryKey"`
    Title       string    `json:"title" binding:"required" gorm:"not null"`
    Description string    `json:"description"`
    Status      string    `json:"status" gorm:"default:pending"`
    DueDate     time.Time `json:"due_date,omitempty"`
    CreatedAt   time.Time `json:"created_at" gorm:"autoCreateTime"`
    UpdatedAt   time.Time `json:"updated_at" gorm:"autoUpdateTime"`
}
```

### Database Connection

```go
// internal/database/db.go
package database

import (
    "github.com/yourusername/windsurf-demo/internal/models"
    "gorm.io/driver/sqlite"
    "gorm.io/gorm"
)

func InitDB() (*gorm.DB, error) {
    db, err := gorm.Open(sqlite.Open("tasks.db"), &gorm.Config{})
    if err != nil {
        return nil, err
    }
    
    // Auto migrate the schema
    err = db.AutoMigrate(&models.Task{})
    if err != nil {
        return nil, err
    }
    
    return db, nil
}
```

### Task Handler

```go
// internal/handlers/task_handler.go
package handlers

import (
    "net/http"
    "strconv"
    
    "github.com/gin-gonic/gin"
    "github.com/yourusername/windsurf-demo/internal/models"
    "gorm.io/gorm"
)

type TaskHandler struct {
    DB *gorm.DB
}

func NewTaskHandler(db *gorm.DB) *TaskHandler {
    return &TaskHandler{DB: db}
}

// ListTasks returns all tasks
func (h *TaskHandler) ListTasks(c *gin.Context) {
    var tasks []models.Task
    
    result := h.DB.Find(&tasks)
    if result.Error != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to fetch tasks"})
        return
    }
    
    c.JSON(http.StatusOK, tasks)
}

// Additional handler methods...
```

## Next Steps

After building your basic API, consider:

1. Adding authentication and authorization
2. Implementing pagination for list endpoints
3. Adding filtering and sorting options
4. Implementing rate limiting
5. Setting up API documentation with Swagger
