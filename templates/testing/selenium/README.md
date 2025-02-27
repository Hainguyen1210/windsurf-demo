# Selenium Test Automation Template

This directory contains a starter template for automated testing using Selenium WebDriver with Python.

## Prerequisites

- Python 3.8+
- Chrome browser
- ChromeDriver (compatible with your Chrome version)

## Setup

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure your application is running at http://localhost:3000

## Running the Tests

Run all tests:
```bash
python -m unittest test_task_manager.py
```

Run a specific test:
```bash
python -m unittest test_task_manager.TaskManagerTest.test_create_task
```

## Test Structure

The template includes:

- Basic setup and teardown methods
- A test for verifying the page title
- A test for creating a new task
- Placeholder tests for updating and deleting tasks

## Using with Windsurf

You can use Windsurf to expand this template into a complete test suite. Here's an example prompt:

```
Expand this Selenium test template to include:
1. Complete implementations for the update and delete task tests
2. Additional tests for task filtering and sorting
3. Tests for form validation
4. Tests for error handling
5. Setup for running tests in a CI/CD pipeline
```
