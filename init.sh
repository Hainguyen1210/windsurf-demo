#!/bin/bash

# Windsurf Demo Initialization Script

echo "Initializing Windsurf Demo Project..."

# Create project name from argument or use default
PROJECT_NAME=${1:-"windsurf-project"}
BRANCH_NAME=${2:-"my-project"}

# Create project directory
mkdir -p $PROJECT_NAME/backend $PROJECT_NAME/frontend

# Copy templates
cp -r templates/backend/* $PROJECT_NAME/backend/
cp -r templates/frontend/* $PROJECT_NAME/frontend/
cp templates/docker-compose.yml $PROJECT_NAME/

# Create README
cat > $PROJECT_NAME/README.md << EOL
# $PROJECT_NAME

This project was created using the Windsurf Demo Starter Kit.

## Getting Started

1. Open this project in Windsurf
2. Follow the prompt guide at: https://github.com/Hainguyen1210/windsurf-demo/blob/main/windsurf_prompt_guide.md

## Project Structure

- \`backend/\`: Go/Gin API
- \`frontend/\`: React frontend
- \`docker-compose.yml\`: Docker configuration
EOL

# Initialize Git repository
cd $PROJECT_NAME
git init
git add .
git commit -m "Initial commit from Windsurf Demo Starter Kit"
git branch -M main
git checkout -b $BRANCH_NAME

echo ""
echo "Project initialized successfully!"
echo "Your new project is in the '$PROJECT_NAME' directory."
echo "A Git repository has been initialized with branches 'main' and '$BRANCH_NAME'."
echo ""
echo "Next steps:"
echo "1. cd $PROJECT_NAME"
echo "2. Open the project in Windsurf"
echo "3. Start building your application using the prompt guide"
