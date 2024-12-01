# AIdirassa Online Platform
![image](https://github.com/user-attachments/assets/5f7f729d-1f34-49bd-a874-d0705afbd0ac)

## Project Overview

The AIdirassa Online platform is a multi-agent powered platform designed to create a fully AI-generated learning pathway. This includes assessments, course pathways, topics, exercises, quizzes, and more. The platform leverages advanced AI agents to provide a personalized and dynamic learning experience.

## Abstract

### Background and Problem Statement
Morocco's education system faces many challenges that hinder its effectiveness and accessibility.
Despite significant government investment, poor infrastructure, teacher shortages, outdated curricula, and socio-economic disparities persist.
![image](https://github.com/user-attachments/assets/7c0949c3-9c62-4ddc-ba9a-d3eb8a6ebdfa)


### Impact and Proposed Solution
The AIdirassa Online platform aims to revolutionize the educational experience by using AI agents to generate personalized learning content. This approach saves time and ensures that each student receives a tailored learning experience that adapts to their progress and needs.

### Project Outcomes and Deliverables
- A fully functional AI-powered learning platform.
- Dynamic generation of learning content including assessments, course pathways, topics, exercises, and quizzes.
- RESTful API endpoints for data management and user interactions.
- Integration of AI models for content generation.
- Efficient database management for user data and progress tracking.

## Workflow

![image](https://github.com/user-attachments/assets/ff766d7a-bb9d-458c-a3c0-0bbbf0297217)

**1. Identify Knowledge**
- **Goal**: Assess the user's current understanding of selecting concepts.
- **Process**:
  - The user expresses interest in X concept.
  - A **Diagnostic Agent** engages with the user by asking multiple-choice questions covering foundational topics such as:
    - What is machine learning?
    - Probability concepts.
  - The diagnostic results help identify the user's knowledge gaps and strengths.
- **Output**: A baseline assessment of the user's current knowledge.

---

**2. Create Your Own Learning Path**
- **Goal**: Construct a tailored learning path based on the diagnostic results.
- **Process**:
  - The platform suggests a **learning path generator** to create a curriculum suitable for the user, offering options like:
    - Basic Introduction to Machine Learning.
    - Focused learning on specific domains like deep learning or probabilistic models.
  - Recommendations for resources include:
    - Tutorials or academic papers.
    - Online videos (e.g., YouTube).
    - External references through web searches.
  - Users can customize their path based on these suggestions.
- **Output**: A personalized learning plan tailored to the user's needs and goals.

---

**3. Evaluation**
- **Goal**: Evaluate the user's progress and mastery of concepts.
- **Process**:
  - Users complete practical **exercises** or **quizzes** designed to test their understanding.
  - The **Agent Quiz Generator** provides dynamic questions for evaluation.
  - Feedback loops help users revisit weak areas if necessary.
- **Output**: Finalized evaluations and progress reports summarizing the user's achievements and next steps.


## Additional Features
- **Save Learning User Status**: Throughout the process, the user's learning status and progress are saved, ensuring continuity in the learning journey.
- **Flexibility**: The system adapts to user needs at every stage by dynamically generating paths and questions.

## Frontend

The frontend of the AIdirassa Online platform is designed to provide an intuitive and engaging user interface. Key features include:

### Technologies Used
![FastApi](https://img.shields.io/badge/JavaScript-F7DF1E.svg?style=for-the-badge&logo=JavaScript&logoColor=black)
![FastApi](https://img.shields.io/badge/HTML5-E34F26.svg?style=for-the-badge&logo=HTML5&logoColor=white)
![FastApi](https://img.shields.io/badge/CSS3-1572B6.svg?style=for-the-badge&logo=CSS3&logoColor=white)

## Backend
The backend of the AIdirassa Online platform handles data processing, AI model integration, and user management. Key components include:

- **API Endpoints:** RESTful APIs to serve data to the frontend and manage user interactions.
- **AI Model Integration:** Integration of trained AI models to generate and update learning content dynamically.
- **Database Management:** Efficient storage and retrieval of user data, learning content, and progress tracking.

### Technologies Used

![FastApi](https://img.shields.io/badge/FastAPI-009688.svg?style=for-the-badge&logo=FastAPI&logoColor=white)
![FastApi](https://img.shields.io/badge/PostgreSQL-4169E1.svg?style=for-the-badge&logo=PostgreSQL&logoColor=white)
![FastApi](https://img.shields.io/badge/LangChain-1C3C3C.svg?style=for-the-badge&logo=LangChain&logoColor=white)
![FastApi](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)
![FastApi](https://img.shields.io/badge/Google%20Colab-F9AB00.svg?style=for-the-badge&logo=Google-Colab&logoColor=white)
![FastApi](https://img.shields.io/badge/Ollama-000000.svg?style=for-the-badge&logo=Ollama&logoColor=white)
## Demo Video

Check out our demo video (Video 1) to see the AIdirassa Online platform in action. The video showcases the user interface, interactive learning modules, and the dynamic content generation powered by AI agents.

## Getting Started

To get started with the AIdirassa Online platform, follow these steps:

1. **Clone the Repository:**
```bash
git clone https://github.com/Elma-dev/aldirassa_online_backend_project.git
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
