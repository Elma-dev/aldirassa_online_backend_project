# AIdirassa Online Platform

## Project Overview

The AIdirassa Online platform is a multi-agent powered platform designed to create a fully AI-generated learning pathway. This includes assessments, course pathways, topics, exercises, quizzes, and more. The platform leverages advanced AI agents to provide a personalized and dynamic learning experience.

## Abstract

### Background and Problem Statement
Morocco's education system faces many challenges that hinder its effectiveness and accessibility. Despite significant government investment, poor infrastructure, teacher shortages, outdated curricula, and socio-economic disparities persist.

### Impact and Proposed Solution
The AIdirassa Online platform aims to revolutionize the educational experience by using AI agents to generate personalized learning content. This approach saves time and ensures that each student receives a tailored learning experience that adapts to their progress and needs.

### Project Outcomes and Deliverables
- A fully functional AI-powered learning platform.
- Dynamic generation of learning content including assessments, course pathways, topics, exercises, and quizzes.
- RESTful API endpoints for data management and user interactions.
- Integration of AI models for content generation.
- Efficient database management for user data and progress tracking.

## Workflow
![image](https://github.com/user-attachments/assets/7b37a4af-0339-4ed2-b876-7891162ed6b0)

## Frontend

The frontend of the AIdirassa Online platform is designed to provide an intuitive and engaging user interface. Key features include:

### Technologies Used

HTML, CSS, JavaScript

## Backend

The backend of the AIdirassa Online platform handles data processing, AI model integration, and user management. Key components include:

- **API Endpoints:** RESTful APIs to serve data to the frontend and manage user interactions.
- **AI Model Integration:** Integration of trained AI models to generate and update learning content dynamically.
- **Database Management:** Efficient storage and retrieval of user data, learning content, and progress tracking.

### Technologies Used

Fast API

## Demo Video

Check out our demo video (Video 1) to see the AIdirassa Online platform in action. The video showcases the user interface, interactive learning modules, and the dynamic content generation powered by AI agents.

## Getting Started

To get started with the AIdirassa Online platform, follow these steps:

1. **Clone the Repository:**
```bash
https://github.com/Elma-dev/aldirassa_online_backend_project.git
```

2. **Navigate to the Project Directory:**
```bash
cd aldirassa_online_backend_project/Backend
```
3. **Create a .env File:**
```bash
touch .env
```
Add the following content to the `.env` file:
```
OPENAI_API_KEY=""
BRAVE_API=""
```

3. **Install the Required Dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the Application:**
```bash
uvicorn main:app --reload
```

5. **Access the Platform:**
Open your web browser and go to [http://localhost:8000](http://localhost:8000) to access the home page (index.html).
