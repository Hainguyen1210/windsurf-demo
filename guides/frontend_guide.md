# Building Frontend Applications with React

This guide will help you use Windsurf to build a modern frontend application using React and TypeScript.

## Overview

React is a popular JavaScript library for building user interfaces, particularly single-page applications. TypeScript adds static type definitions to JavaScript, enhancing code quality and developer experience.

## Getting Started with Windsurf

Here's how to use Windsurf to create your React frontend:

1. Open your project in Windsurf
2. Use the following prompts to get started

## Sample Prompts for Windsurf

### Setting Up the Project

```
Create a new React application with TypeScript. Set up the basic project structure with:
- A components directory for React components
- A services directory for API services
- A types directory for TypeScript interfaces
```

### Creating TypeScript Types

```
Create TypeScript interfaces for the Task model with the following properties:
- id (number)
- title (string)
- description (string)
- status (string)
- due_date (optional string)
- created_at (string)
- updated_at (string)

Also create interfaces for TaskCreate and TaskUpdate operations.
```

### Creating API Services

```
Create an API service using Axios to connect to our Go backend. Implement functions for:
- Fetching all tasks
- Fetching a single task by ID
- Creating a new task
- Updating an existing task
- Deleting a task
```

### Building React Components

```
Create a TaskForm component that:
- Accepts initial values and an onSubmit callback
- Handles form input for task title, description, status, and due date
- Validates required fields
- Submits the form data to the parent component
```

```
Create a TaskItem component that:
- Displays a single task with all its details
- Provides buttons for editing and deleting
- Shows different styling based on task status
- Expands to show the edit form when in edit mode
```

```
Create a TaskList component that:
- Fetches and displays all tasks
- Handles creating new tasks
- Passes update and delete handlers to TaskItem components
- Shows loading states and error messages
```

### Creating the Main Application

```
Create the App component that:
- Sets up the overall layout with header, main content, and footer
- Includes the TaskList component
- Provides global styling
```

### Adding CSS Styles

```
Create a styles.css file with:
- A clean, modern design
- Responsive layout
- Styling for forms, buttons, and task items
- Visual indicators for different task statuses
```

## Project Structure

A typical React frontend project structure looks like this:

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

## Best Practices

1. **Component organization**: Keep components small and focused on a single responsibility
2. **Type safety**: Use TypeScript interfaces for all data structures
3. **API abstraction**: Isolate API calls in service modules
4. **Error handling**: Properly handle loading states and errors
5. **Responsive design**: Ensure the UI works well on different screen sizes
6. **Accessibility**: Follow accessibility best practices for forms and interactive elements

## Example Code Snippets

### TypeScript Types

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

### API Service

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

### React Component

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

  // Component JSX...
};

export default TaskItem;
```

## Next Steps

After building your basic frontend, consider:

1. Adding user authentication UI
2. Implementing state management with Redux or Context API
3. Adding routing with React Router
4. Implementing form validation with Formik or React Hook Form
5. Adding animations and transitions
6. Implementing dark mode or theme switching
