# Go Gin API Implementation Plan

## Project Structure

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

## Implementation Steps

### 1. Initialize Go Module

```bash
mkdir -p backend/cmd/api backend/internal/{database,handlers,middleware,models} backend/tests
cd backend
go mod init github.com/yourusername/windsurf-demo
go get -u github.com/gin-gonic/gin
go get -u gorm.io/gorm
go get -u gorm.io/driver/sqlite
```

### 2. Define Task Model

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

type TaskCreate struct {
    Title       string    `json:"title" binding:"required"`
    Description string    `json:"description"`
    Status      string    `json:"status"`
    DueDate     time.Time `json:"due_date,omitempty"`
}

type TaskUpdate struct {
    Title       string    `json:"title"`
    Description string    `json:"description"`
    Status      string    `json:"status"`
    DueDate     time.Time `json:"due_date,omitempty"`
}
```

### 3. Set Up Database Connection

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

### 4. Implement Task Handlers

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

// GetTask returns a task by ID
func (h *TaskHandler) GetTask(c *gin.Context) {
    id, err := strconv.Atoi(c.Param("id"))
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid task ID"})
        return
    }
    
    var task models.Task
    result := h.DB.First(&task, id)
    if result.Error != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": "Task not found"})
        return
    }
    
    c.JSON(http.StatusOK, task)
}

// CreateTask creates a new task
func (h *TaskHandler) CreateTask(c *gin.Context) {
    var taskCreate models.TaskCreate
    
    if err := c.ShouldBindJSON(&taskCreate); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    
    task := models.Task{
        Title:       taskCreate.Title,
        Description: taskCreate.Description,
        Status:      taskCreate.Status,
        DueDate:     taskCreate.DueDate,
    }
    
    result := h.DB.Create(&task)
    if result.Error != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create task"})
        return
    }
    
    c.JSON(http.StatusCreated, task)
}

// UpdateTask updates a task by ID
func (h *TaskHandler) UpdateTask(c *gin.Context) {
    id, err := strconv.Atoi(c.Param("id"))
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid task ID"})
        return
    }
    
    var task models.Task
    result := h.DB.First(&task, id)
    if result.Error != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": "Task not found"})
        return
    }
    
    var taskUpdate models.TaskUpdate
    if err := c.ShouldBindJSON(&taskUpdate); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    
    // Update fields if provided
    if taskUpdate.Title != "" {
        task.Title = taskUpdate.Title
    }
    if taskUpdate.Description != "" {
        task.Description = taskUpdate.Description
    }
    if taskUpdate.Status != "" {
        task.Status = taskUpdate.Status
    }
    if !taskUpdate.DueDate.IsZero() {
        task.DueDate = taskUpdate.DueDate
    }
    
    h.DB.Save(&task)
    
    c.JSON(http.StatusOK, task)
}

// DeleteTask deletes a task by ID
func (h *TaskHandler) DeleteTask(c *gin.Context) {
    id, err := strconv.Atoi(c.Param("id"))
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid task ID"})
        return
    }
    
    result := h.DB.Delete(&models.Task{}, id)
    if result.Error != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to delete task"})
        return
    }
    
    if result.RowsAffected == 0 {
        c.JSON(http.StatusNotFound, gin.H{"error": "Task not found"})
        return
    }
    
    c.JSON(http.StatusOK, gin.H{"message": "Task deleted successfully"})
}
```

### 5. Implement Middleware

```go
// internal/middleware/logger.go
package middleware

import (
    "time"
    
    "github.com/gin-gonic/gin"
)

func Logger() gin.HandlerFunc {
    return func(c *gin.Context) {
        start := time.Now()
        
        // Process request
        c.Next()
        
        // Log request details
        latency := time.Since(start)
        status := c.Writer.Status()
        
        gin.DefaultWriter.Write([]byte(
            "| " + c.Request.Method + " | " +
            c.Request.URL.Path + " | " +
            strconv.Itoa(status) + " | " +
            latency.String() + " |\n",
        ))
    }
}

// internal/middleware/cors.go
package middleware

import "github.com/gin-gonic/gin"

func CORS() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
        c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
        c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
        c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT, DELETE")

        if c.Request.Method == "OPTIONS" {
            c.AbortWithStatus(204)
            return
        }

        c.Next()
    }
}
```

### 6. Create Main Application

```go
// cmd/api/main.go
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
    log.Println("Starting server on :8080")
    r.Run(":8080")
}
```

### 7. Write Tests

```go
// tests/handlers_test.go
package tests

import (
    "bytes"
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"
    
    "github.com/gin-gonic/gin"
    "github.com/stretchr/testify/assert"
    "github.com/yourusername/windsurf-demo/internal/database"
    "github.com/yourusername/windsurf-demo/internal/handlers"
    "github.com/yourusername/windsurf-demo/internal/models"
)

func setupTestRouter() (*gin.Engine, *handlers.TaskHandler) {
    gin.SetMode(gin.TestMode)
    
    // Use in-memory SQLite for testing
    db, _ := database.InitDB()
    
    // Clear tasks table
    db.Exec("DELETE FROM tasks")
    
    taskHandler := handlers.NewTaskHandler(db)
    
    r := gin.Default()
    api := r.Group("/api/v1")
    tasks := api.Group("/tasks")
    {
        tasks.GET("", taskHandler.ListTasks)
        tasks.GET("/:id", taskHandler.GetTask)
        tasks.POST("", taskHandler.CreateTask)
        tasks.PUT("/:id", taskHandler.UpdateTask)
        tasks.DELETE("/:id", taskHandler.DeleteTask)
    }
    
    return r, taskHandler
}

func TestCreateTask(t *testing.T) {
    r, _ := setupTestRouter()
    
    taskCreate := models.TaskCreate{
        Title:       "Test Task",
        Description: "This is a test task",
        Status:      "pending",
    }
    
    jsonValue, _ := json.Marshal(taskCreate)
    req, _ := http.NewRequest("POST", "/api/v1/tasks", bytes.NewBuffer(jsonValue))
    w := httptest.NewRecorder()
    r.ServeHTTP(w, req)
    
    assert.Equal(t, http.StatusCreated, w.Code)
    
    var response models.Task
    err := json.Unmarshal(w.Body.Bytes(), &response)
    assert.NoError(t, err)
    assert.Equal(t, taskCreate.Title, response.Title)
    assert.Equal(t, taskCreate.Description, response.Description)
    assert.Equal(t, taskCreate.Status, response.Status)
    assert.NotZero(t, response.ID)
}

// Add more tests for other endpoints...
```

### 8. Create Dockerfile

```dockerfile
# Dockerfile
FROM golang:1.16-alpine AS builder

WORKDIR /app

# Copy go mod and sum files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY . .

# Build the application
RUN CGO_ENABLED=1 GOOS=linux go build -a -o api ./cmd/api

# Final stage
FROM alpine:latest

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

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/tasks | List all tasks |
| GET | /api/v1/tasks/:id | Get task by ID |
| POST | /api/v1/tasks | Create new task |
| PUT | /api/v1/tasks/:id | Update task |
| DELETE | /api/v1/tasks/:id | Delete task |

## Testing the API

```bash
# Create a task
curl -X POST http://localhost:8080/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries","description":"Milk, eggs, bread","status":"pending"}'

# Get all tasks
curl http://localhost:8080/api/v1/tasks

# Get a specific task
curl http://localhost:8080/api/v1/tasks/1

# Update a task
curl -X PUT http://localhost:8080/api/v1/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"completed"}'

# Delete a task
curl -X DELETE http://localhost:8080/api/v1/tasks/1
```
