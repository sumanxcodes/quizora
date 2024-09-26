
# Quizora

This repository contains the backend for Quizora Python based game using Django. The backend is designed to provide a RestFul API (API app) and interactive platform for students, teachers, and administrators. It allows users to create, manage, and participate in quizzes tailored to educational purposes, with a focus on arithmetic quizzes. The app is built with a clean and scalable structure, leveraging Django's robust framework for rapid development and deployment.

## Features

- **Role-Based Access Control**: 
  - **Admin**: Can manage users, quizzes, and view reports.
  - **Teacher**: Can create and manage quiz questions.
  - **Student**: Can participate in quizzes and view their scores.
  
- **User Management**:
  - Supports different user roles (admin, teacher, and student).
  - Allows for account creation, login, and role-based access.
  
- **Quiz Creation**:
  - Teachers can create quizzes by adding multiple-choice questions with options.
  - Quizzes are stored in a database for easy management and retrieval.

- **Game Sessions**:
  - Students can participate in quizzes and their results are stored in game sessions.
  - Scores are calculated based on correct answers and displayed at the end of the session.

- **Dynamic Question Management**:
  - Teachers can add, edit, and delete questions with flexible options (e.g., multiple-choice).
  
- **Security**:
  - Uses environment variables to protect sensitive data like the Django `SECRET_KEY`.
  - Role-based permissions ensure that only authorized users have access to certain features.

## Technology Stack

- **Backend**: Django (Python) – a high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **Database**: SQLite (for development), with the ability to switch to PostgreSQL, MySQL, or other databases for production.
- **Frontend**: Basic Django templates (HTML, CSS) for displaying the quiz interface.
- **Environment Management**: Python-decouple for environment variable management, ensuring security and scalability.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/quizora.git
   cd quizora
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the `.env` file:
   ```bash
   touch .env
   ```

   Add the following in `.env`:
   ```
   SECRET_KEY='your-secret-key-here'
   ```

4. Run database migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application at `http://127.0.0.1:8000/`.

## Future Enhancements

- **Real-time Analytics**: Add real-time quiz analytics and reporting for teachers and administrators.
- **Leaderboards**: Implement global and class-based leaderboards to track top-performing students.
- **Question Bank**: Add support for multiple types of questions (e.g., short answer, true/false) and the ability to categorize questions by difficulty level.
- **API Integration**: Build REST or GraphQL APIs to integrate with other educational platforms.
