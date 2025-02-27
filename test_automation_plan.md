# Test Automation Plan

This plan outlines the approach for implementing comprehensive test automation for both the Go backend API and React frontend application.

## Backend Testing Strategy

### 1. Unit Tests

Unit tests focus on testing individual functions and methods in isolation.

#### Example Unit Test for Task Model

```go
// internal/models/task_test.go
package models

import (
    "testing"
    "time"
)

func TestTaskValidation(t *testing.T) {
    // Test case: Valid task
    task := Task{
        Title:       "Test Task",
        Description: "This is a test task",
        Status:      "pending",
    }
    
    // Add validation logic test here
    if task.Title == "" {
        t.Error("Expected title to be set")
    }
    
    // Test case: Invalid task (empty title)
    invalidTask := Task{
        Description: "This is an invalid task",
        Status:      "pending",
    }
    
    // Add validation logic test here
    if invalidTask.Title != "" {
        t.Error("Expected title to be empty")
    }
}
```

### 2. Integration Tests

Integration tests verify that different parts of the application work together correctly.

#### Example Integration Test for Task Handler

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
    req.Header.Set("Content-Type", "application/json")
    
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

func TestGetTask(t *testing.T) {
    r, _ := setupTestRouter()
    
    // First create a task
    taskCreate := models.TaskCreate{
        Title:       "Test Task",
        Description: "This is a test task",
        Status:      "pending",
    }
    
    jsonValue, _ := json.Marshal(taskCreate)
    req, _ := http.NewRequest("POST", "/api/v1/tasks", bytes.NewBuffer(jsonValue))
    req.Header.Set("Content-Type", "application/json")
    
    w := httptest.NewRecorder()
    r.ServeHTTP(w, req)
    
    var createdTask models.Task
    json.Unmarshal(w.Body.Bytes(), &createdTask)
    
    // Now get the task by ID
    req, _ = http.NewRequest("GET", "/api/v1/tasks/"+strconv.Itoa(int(createdTask.ID)), nil)
    w = httptest.NewRecorder()
    r.ServeHTTP(w, req)
    
    assert.Equal(t, http.StatusOK, w.Code)
    
    var fetchedTask models.Task
    err := json.Unmarshal(w.Body.Bytes(), &fetchedTask)
    assert.NoError(t, err)
    assert.Equal(t, createdTask.ID, fetchedTask.ID)
    assert.Equal(t, createdTask.Title, fetchedTask.Title)
}

// Additional tests for update, delete, and list operations...
```

### 3. API Tests

API tests verify that the API endpoints behave as expected from an external client's perspective.

#### Example API Test Using Go's Testing Package

```go
// tests/api_test.go
package tests

import (
    "bytes"
    "encoding/json"
    "fmt"
    "net/http"
    "os"
    "testing"
    
    "github.com/stretchr/testify/assert"
    "github.com/yourusername/windsurf-demo/internal/models"
)

var baseURL = "http://localhost:8080/api/v1"

func TestMain(m *testing.M) {
    // Start the server in a goroutine
    go func() {
        main()
    }()
    
    // Wait for the server to start
    time.Sleep(2 * time.Second)
    
    // Run the tests
    exitCode := m.Run()
    
    // Exit with the same code
    os.Exit(exitCode)
}

func TestAPICreateTask(t *testing.T) {
    taskCreate := models.TaskCreate{
        Title:       "API Test Task",
        Description: "This is a test task created via API test",
        Status:      "pending",
    }
    
    jsonValue, _ := json.Marshal(taskCreate)
    resp, err := http.Post(
        fmt.Sprintf("%s/tasks", baseURL),
        "application/json",
        bytes.NewBuffer(jsonValue),
    )
    
    assert.NoError(t, err)
    assert.Equal(t, http.StatusCreated, resp.StatusCode)
    
    var createdTask models.Task
    json.NewDecoder(resp.Body).Decode(&createdTask)
    resp.Body.Close()
    
    assert.Equal(t, taskCreate.Title, createdTask.Title)
    assert.Equal(t, taskCreate.Description, createdTask.Description)
    assert.Equal(t, taskCreate.Status, createdTask.Status)
    assert.NotZero(t, createdTask.ID)
    
    // Cleanup: Delete the created task
    req, _ := http.NewRequest(
        "DELETE",
        fmt.Sprintf("%s/tasks/%d", baseURL, createdTask.ID),
        nil,
    )
    
    client := &http.Client{}
    resp, err = client.Do(req)
    assert.NoError(t, err)
    assert.Equal(t, http.StatusOK, resp.StatusCode)
}

// Additional API tests...
```

## Frontend Testing Strategy

### 1. Unit Tests

Unit tests for React components focus on testing individual components in isolation.

#### Example Unit Test for TaskForm Component

```jsx
// src/components/TaskForm.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import TaskForm from './TaskForm';

describe('TaskForm', () => {
  test('renders form elements correctly', () => {
    render(<TaskForm onSubmit={jest.fn()} />);
    
    expect(screen.getByLabelText(/title/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/status/i)).toBeInTheDocument();
    expect(screen.getByText(/add task/i)).toBeInTheDocument();
  });
  
  test('submits form with correct data', () => {
    const mockSubmit = jest.fn();
    render(<TaskForm onSubmit={mockSubmit} />);
    
    // Fill out the form
    fireEvent.change(screen.getByLabelText(/title/i), {
      target: { value: 'Test Task' },
    });
    
    fireEvent.change(screen.getByLabelText(/description/i), {
      target: { value: 'Test Description' },
    });
    
    fireEvent.change(screen.getByLabelText(/status/i), {
      target: { value: 'in_progress' },
    });
    
    // Submit the form
    fireEvent.click(screen.getByText(/add task/i));
    
    // Check if onSubmit was called with the correct data
    expect(mockSubmit).toHaveBeenCalledWith({
      title: 'Test Task',
      description: 'Test Description',
      status: 'in_progress',
      due_date: '',
    });
  });
  
  test('validates required fields', () => {
    const mockSubmit = jest.fn();
    render(<TaskForm onSubmit={mockSubmit} />);
    
    // Submit without filling out required fields
    fireEvent.click(screen.getByText(/add task/i));
    
    // Check if form validation works (onSubmit should not be called)
    expect(mockSubmit).not.toHaveBeenCalled();
  });
});
```

### 2. Integration Tests

Integration tests for the frontend verify that components work together correctly.

#### Example Integration Test for TaskList Component

```jsx
// src/components/TaskList.test.tsx
import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import TaskList from './TaskList';

// Mock API responses
const server = setupServer(
  // GET /tasks
  rest.get('http://localhost:8080/api/v1/tasks', (req, res, ctx) => {
    return res(
      ctx.json([
        {
          id: 1,
          title: 'Test Task 1',
          description: 'Description 1',
          status: 'pending',
          created_at: '2023-01-01T00:00:00Z',
          updated_at: '2023-01-01T00:00:00Z',
        },
        {
          id: 2,
          title: 'Test Task 2',
          description: 'Description 2',
          status: 'completed',
          created_at: '2023-01-02T00:00:00Z',
          updated_at: '2023-01-02T00:00:00Z',
        },
      ])
    );
  }),
  
  // POST /tasks
  rest.post('http://localhost:8080/api/v1/tasks', (req, res, ctx) => {
    return res(
      ctx.status(201),
      ctx.json({
        id: 3,
        ...req.body,
        created_at: '2023-01-03T00:00:00Z',
        updated_at: '2023-01-03T00:00:00Z',
      })
    );
  }),
  
  // Other API endpoints...
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('TaskList', () => {
  test('loads and displays tasks', async () => {
    render(<TaskList />);
    
    // Initially should show loading state
    expect(screen.getByText(/loading tasks/i)).toBeInTheDocument();
    
    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Test Task 1')).toBeInTheDocument();
      expect(screen.getByText('Test Task 2')).toBeInTheDocument();
    });
  });
  
  test('creates a new task', async () => {
    render(<TaskList />);
    
    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Test Task 1')).toBeInTheDocument();
    });
    
    // Fill out the form
    fireEvent.change(screen.getByLabelText(/title/i), {
      target: { value: 'New Test Task' },
    });
    
    fireEvent.change(screen.getByLabelText(/description/i), {
      target: { value: 'New Description' },
    });
    
    // Submit the form
    fireEvent.click(screen.getByText(/add task/i));
    
    // Should show loading state again
    expect(screen.getByText(/loading tasks/i)).toBeInTheDocument();
    
    // Wait for tasks to reload
    await waitFor(() => {
      expect(screen.getByText('New Test Task')).toBeInTheDocument();
    });
  });
  
  // Additional tests for updating and deleting tasks...
});
```

### 3. End-to-End Tests

End-to-end tests verify that the entire application works correctly from a user's perspective.

#### Example E2E Test Using Cypress

```javascript
// cypress/integration/tasks.spec.js
describe('Task Manager Application', () => {
  beforeEach(() => {
    // Visit the application
    cy.visit('http://localhost:3000');
    
    // Clear tasks from the database (via API)
    cy.request('DELETE', 'http://localhost:8080/api/v1/tasks/all');
  });
  
  it('should display the task list', () => {
    cy.contains('Task Manager');
    cy.contains('Add New Task');
    cy.contains('Your Tasks');
    cy.contains('No tasks found');
  });
  
  it('should create a new task', () => {
    // Fill out the form
    cy.get('input[name="title"]').type('Cypress Test Task');
    cy.get('textarea[name="description"]').type('This task was created by Cypress');
    cy.get('select[name="status"]').select('in_progress');
    
    // Submit the form
    cy.contains('Add Task').click();
    
    // Verify the task was created
    cy.contains('Cypress Test Task');
    cy.contains('This task was created by Cypress');
    cy.contains('in progress');
  });
  
  it('should update a task', () => {
    // Create a task first
    cy.get('input[name="title"]').type('Task to Update');
    cy.get('textarea[name="description"]').type('This task will be updated');
    cy.contains('Add Task').click();
    
    // Click edit button
    cy.contains('Task to Update')
      .parent()
      .parent()
      .contains('Edit')
      .click();
    
    // Update the task
    cy.get('input[name="title"]').clear().type('Updated Task');
    cy.get('select[name="status"]').select('completed');
    
    // Submit the update
    cy.contains('Update Task').click();
    
    // Verify the task was updated
    cy.contains('Updated Task');
    cy.contains('completed');
  });
  
  it('should delete a task', () => {
    // Create a task first
    cy.get('input[name="title"]').type('Task to Delete');
    cy.contains('Add Task').click();
    
    // Verify the task exists
    cy.contains('Task to Delete');
    
    // Delete the task
    cy.contains('Task to Delete')
      .parent()
      .parent()
      .contains('Delete')
      .click();
    
    // Confirm the deletion
    cy.on('window:confirm', () => true);
    
    // Verify the task was deleted
    cy.contains('Task to Delete').should('not.exist');
  });
});
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Go
        uses: actions/setup-go@v2
        with:
          go-version: 1.16
      
      - name: Install dependencies
        run: |
          cd backend
          go mod download
      
      - name: Run tests
        run: |
          cd backend
          go test -v ./...
  
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '14'
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Run tests
        run: |
          cd frontend
          npm test -- --watchAll=false
  
  e2e-tests:
    runs-on: ubuntu-latest
    needs: [backend-tests, frontend-tests]
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Docker Compose
        run: |
          docker-compose build
          docker-compose up -d
      
      - name: Wait for services to start
        run: sleep 10
      
      - name: Run Cypress tests
        uses: cypress-io/github-action@v2
        with:
          working-directory: frontend
          start: npm start
          wait-on: 'http://localhost:3000'
      
      - name: Stop Docker Compose
        run: docker-compose down
  
  build-and-deploy:
    runs-on: ubuntu-latest
    needs: [e2e-tests]
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v2
      
      - name: Build and push Docker images
        run: |
          docker-compose build
          # Add deployment steps here
```

## Test Coverage and Reporting

### Backend Test Coverage

```bash
cd backend
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out -o coverage.html
```

### Frontend Test Coverage

```bash
cd frontend
npm test -- --coverage --watchAll=false
```

## Test Automation Best Practices

1. **Test Pyramid**: Follow the test pyramid approach with more unit tests, fewer integration tests, and even fewer E2E tests.
2. **Isolation**: Ensure tests are isolated and don't depend on each other.
3. **Mocking**: Use mocks for external dependencies to ensure tests are deterministic.
4. **Continuous Integration**: Run tests automatically on every code change.
5. **Test Data**: Use fixtures or factories to generate test data.
6. **Assertions**: Use clear and specific assertions.
7. **Clean Up**: Clean up test data after tests run.

## Additional Testing Considerations

1. **Performance Testing**: Use tools like k6 or JMeter to test API performance.
2. **Security Testing**: Implement security scanning with tools like OWASP ZAP.
3. **Accessibility Testing**: Use tools like axe or Lighthouse for accessibility testing.
4. **Visual Regression Testing**: Consider tools like Percy for visual regression testing.
5. **Contract Testing**: Implement contract tests between frontend and backend.
