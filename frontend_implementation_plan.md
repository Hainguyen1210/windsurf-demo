# React Frontend Implementation Plan

## Project Structure

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── TaskForm.tsx
│   │   ├── TaskItem.tsx
│   │   └── TaskList.tsx
│   ├── services/
│   │   └── api.ts
│   ├── types/
│   │   └── index.ts
│   ├── App.tsx
│   ├── index.tsx
│   └── styles.css
├── package.json
├── tsconfig.json
└── Dockerfile
```

## Implementation Steps

### 1. Initialize React Application

```bash
npx create-react-app frontend --template typescript
cd frontend
npm install axios react-router-dom @types/react-router-dom
```

### 2. Define TypeScript Types

```typescript
// src/types/index.ts
export interface Task {
  id: number;
  title: string;
  description: string;
  status: string;
  due_date?: string;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description: string;
  status: string;
  due_date?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  status?: string;
  due_date?: string;
}
```

### 3. Create API Service

```typescript
// src/services/api.ts
import axios from 'axios';
import { Task, TaskCreate, TaskUpdate } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchTasks = async (): Promise<Task[]> => {
  const response = await api.get('/tasks');
  return response.data;
};

export const fetchTask = async (id: number): Promise<Task> => {
  const response = await api.get(`/tasks/${id}`);
  return response.data;
};

export const createTask = async (task: TaskCreate): Promise<Task> => {
  const response = await api.post('/tasks', task);
  return response.data;
};

export const updateTask = async (id: number, task: TaskUpdate): Promise<Task> => {
  const response = await api.put(`/tasks/${id}`, task);
  return response.data;
};

export const deleteTask = async (id: number): Promise<void> => {
  await api.delete(`/tasks/${id}`);
};
```

### 4. Create Task Components

#### Task Form Component

```tsx
// src/components/TaskForm.tsx
import React, { useState } from 'react';
import { TaskCreate } from '../types';

interface TaskFormProps {
  onSubmit: (task: TaskCreate) => void;
  initialValues?: TaskCreate;
  buttonText?: string;
}

const TaskForm: React.FC<TaskFormProps> = ({
  onSubmit,
  initialValues = { title: '', description: '', status: 'pending' },
  buttonText = 'Add Task',
}) => {
  const [task, setTask] = useState<TaskCreate>(initialValues);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setTask((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(task);
    if (!initialValues.title) {
      // Reset form if it's a new task
      setTask({ title: '', description: '', status: 'pending' });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="task-form">
      <div className="form-group">
        <label htmlFor="title">Title</label>
        <input
          type="text"
          id="title"
          name="title"
          value={task.title}
          onChange={handleChange}
          required
          placeholder="Task title"
        />
      </div>
      
      <div className="form-group">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          name="description"
          value={task.description}
          onChange={handleChange}
          placeholder="Task description"
          rows={3}
        />
      </div>
      
      <div className="form-group">
        <label htmlFor="status">Status</label>
        <select
          id="status"
          name="status"
          value={task.status}
          onChange={handleChange}
        >
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
      </div>
      
      <div className="form-group">
        <label htmlFor="due_date">Due Date (Optional)</label>
        <input
          type="date"
          id="due_date"
          name="due_date"
          value={task.due_date || ''}
          onChange={handleChange}
        />
      </div>
      
      <button type="submit" className="btn-primary">{buttonText}</button>
    </form>
  );
};

export default TaskForm;
```

#### Task Item Component

```tsx
// src/components/TaskItem.tsx
import React, { useState } from 'react';
import { Task, TaskUpdate } from '../types';
import TaskForm from './TaskForm';

interface TaskItemProps {
  task: Task;
  onUpdate: (id: number, task: TaskUpdate) => void;
  onDelete: (id: number) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onUpdate, onDelete }) => {
  const [isEditing, setIsEditing] = useState(false);

  const handleUpdate = (updatedTask: TaskUpdate) => {
    onUpdate(task.id, updatedTask);
    setIsEditing(false);
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'Not set';
    return new Date(dateString).toLocaleDateString();
  };

  const getStatusClass = (status: string) => {
    switch (status) {
      case 'completed':
        return 'status-completed';
      case 'in_progress':
        return 'status-in-progress';
      default:
        return 'status-pending';
    }
  };

  if (isEditing) {
    return (
      <div className="task-item editing">
        <TaskForm
          initialValues={{
            title: task.title,
            description: task.description,
            status: task.status,
            due_date: task.due_date,
          }}
          onSubmit={handleUpdate}
          buttonText="Update Task"
        />
        <button 
          className="btn-secondary" 
          onClick={() => setIsEditing(false)}
        >
          Cancel
        </button>
      </div>
    );
  }

  return (
    <div className="task-item">
      <div className="task-header">
        <h3>{task.title}</h3>
        <span className={`status-badge ${getStatusClass(task.status)}`}>
          {task.status.replace('_', ' ')}
        </span>
      </div>
      
      <p className="task-description">{task.description || 'No description'}</p>
      
      <div className="task-meta">
        <span>Due: {formatDate(task.due_date)}</span>
        <span>Created: {formatDate(task.created_at)}</span>
      </div>
      
      <div className="task-actions">
        <button 
          className="btn-primary" 
          onClick={() => setIsEditing(true)}
        >
          Edit
        </button>
        <button 
          className="btn-danger" 
          onClick={() => onDelete(task.id)}
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default TaskItem;
```

#### Task List Component

```tsx
// src/components/TaskList.tsx
import React, { useState, useEffect } from 'react';
import { fetchTasks, createTask, updateTask, deleteTask } from '../services/api';
import { Task, TaskCreate, TaskUpdate } from '../types';
import TaskForm from './TaskForm';
import TaskItem from './TaskItem';

const TaskList: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
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

  const handleCreateTask = async (taskData: TaskCreate) => {
    try {
      setLoading(true);
      await createTask(taskData);
      await loadTasks();
    } catch (err) {
      setError('Failed to create task');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateTask = async (id: number, taskData: TaskUpdate) => {
    try {
      setLoading(true);
      await updateTask(id, taskData);
      await loadTasks();
    } catch (err) {
      setError('Failed to update task');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTask = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }
    
    try {
      setLoading(true);
      await deleteTask(id);
      await loadTasks();
    } catch (err) {
      setError('Failed to delete task');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="task-list-container">
      <h2>Task Manager</h2>
      
      <div className="new-task-section">
        <h3>Add New Task</h3>
        <TaskForm onSubmit={handleCreateTask} />
      </div>
      
      {error && <div className="error-message">{error}</div>}
      
      <div className="tasks-section">
        <h3>Your Tasks</h3>
        {loading ? (
          <div className="loading">Loading tasks...</div>
        ) : tasks.length === 0 ? (
          <div className="empty-state">No tasks found. Create your first task above!</div>
        ) : (
          <div className="tasks-grid">
            {tasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onUpdate={handleUpdateTask}
                onDelete={handleDeleteTask}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default TaskList;
```

### 5. Create App Component

```tsx
// src/App.tsx
import React from 'react';
import TaskList from './components/TaskList';
import './styles.css';

const App: React.FC = () => {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Task Manager</h1>
        <p>A simple task management application</p>
      </header>
      
      <main className="app-main">
        <TaskList />
      </main>
      
      <footer className="app-footer">
        <p>Task Manager Demo &copy; {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
};

export default App;
```

### 6. Add CSS Styles

```css
/* src/styles.css */
:root {
  --primary-color: #4a6fa5;
  --secondary-color: #166088;
  --accent-color: #4fc08d;
  --danger-color: #e15554;
  --text-color: #333;
  --light-text: #666;
  --background-color: #f5f7fa;
  --card-background: #fff;
  --border-color: #ddd;
  --shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: var(--background-color);
  color: var(--text-color);
  line-height: 1.6;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  background-color: var(--primary-color);
  color: white;
  padding: 1.5rem;
  text-align: center;
}

.app-main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.app-footer {
  background-color: var(--secondary-color);
  color: white;
  padding: 1rem;
  text-align: center;
}

/* Task List Styles */
.task-list-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.new-task-section, .tasks-section {
  background-color: var(--card-background);
  border-radius: 8px;
  box-shadow: var(--shadow);
  padding: 1.5rem;
}

.tasks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

/* Task Item Styles */
.task-item {
  background-color: var(--card-background);
  border-radius: 8px;
  box-shadow: var(--shadow);
  padding: 1.5rem;
  border-left: 4px solid var(--primary-color);
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.task-item.editing {
  border-left-color: var(--accent-color);
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.task-description {
  color: var(--light-text);
  flex: 1;
}

.task-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  color: var(--light-text);
}

.task-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.status-badge {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  text-transform: capitalize;
}

.status-pending {
  background-color: #ffeeba;
  color: #856404;
}

.status-in-progress {
  background-color: #b8daff;
  color: #004085;
}

.status-completed {
  background-color: #c3e6cb;
  color: #155724;
}

/* Form Styles */
.task-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: 600;
}

input, textarea, select {
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-family: inherit;
  font-size: 1rem;
}

/* Button Styles */
button {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
}

.btn-primary:hover {
  background-color: var(--secondary-color);
}

.btn-secondary {
  background-color: #e9ecef;
  color: var(--text-color);
}

.btn-secondary:hover {
  background-color: #dee2e6;
}

.btn-danger {
  background-color: var(--danger-color);
  color: white;
}

.btn-danger:hover {
  background-color: #c82333;
}

/* Utility Styles */
.loading {
  text-align: center;
  padding: 2rem;
  color: var(--light-text);
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: var(--light-text);
  background-color: #f8f9fa;
  border-radius: 8px;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}
```

### 7. Create Dockerfile

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

# Build the application
RUN npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:alpine

# Copy the build output to replace the default nginx contents
COPY --from=build /app/build /usr/share/nginx/html

# Copy custom nginx config if needed
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
```

## Testing the Frontend

```bash
# Start the development server
npm start

# Run tests
npm test

# Build for production
npm run build
```

## Integration with Backend

To ensure the frontend communicates properly with the backend:

1. Make sure the API URL is correctly set in the environment variables or directly in the code
2. Ensure CORS is properly configured on the backend
3. Test all API endpoints from the frontend
4. Handle loading states and errors appropriately

## Additional Features to Consider

1. **Authentication**: Add user login/registration
2. **Filtering and Sorting**: Allow users to filter tasks by status or sort by due date
3. **Pagination**: Implement pagination for large task lists
4. **Dark Mode**: Add a theme toggle for light/dark mode
5. **Responsive Design**: Ensure the UI works well on mobile devices
