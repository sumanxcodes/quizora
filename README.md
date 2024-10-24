

# Quizora

This repository is a backend for Quizora, a Python-based desktop quiz game. This backend service is built using the Django Web framework for Python. 
 RESTful API. 
2. **[RestFul API](#restful-api)**: Serves as a communication service between the Game and the Database using API endpoints. It is built using Django's Rest Framework for rapid development and deployment.

## Restful API
### Features
1. **Role-Based Access Control**
	  - **Admin**: Can manage users (teachers and student)
	  - **Teacher**: Can create and manage quiz questions.
	  - **Student**: Can participate in quizzes (Game Session) and view their scores.
  
2. **User Management**
	  -  User roles (admin, teacher, and student).
	  -  Account creation, login, and role-based access. 
		  ```  
			API endpoint
			localhost:8080/admin  
			``` 
**Endpoint: localhost:8080/admin**
  
3.  **Quiz Creation**
	  - Teachers can create quizzes based on category and further add questions to the quizzes
	  - Quizzes and questions are stored in a sqlite for easy access.
		```  
		API endpoints 
		localhost:8080/api/quizzes  
		localhost:8080/api/questions
		``` 

4. **Game Sessions**:
	  - Students can participate in quizzes and their results are stored in game sessions.
	  - Scores are calculated based on correct answers and total score is displayed at the end of the session.
		  ```  
		API endpoint 
		localhost:8080/api/gamesessions  
		``` 

5. **Leaderboard**:
	- Students can view their position on leaderboard
	- Leaderboard is maintained between students of same class year
		 ```  
		API endpoint 
		localhost:8080/api/leaderboard 
		``` 
6. **Progress Tracking**:
	- Student can login to the dashboard to view their overall perfromance on the quizzes based on category 
	- Teacher can view his/her students progress in the dashboard 
		 ```  
		API endpoint 
		localhost:8080/api/progresstracking  
		``` 


## Technology Stack

1.  **Backend (Dashboard and API)**: _Django (Python)_, a high-level Python web framework.  _Django REST framework_, a powerful and flexible tool for building Web APIs. (Trust us it is amazing... Best for rapid prototyping)
- **Database**: SQLite (for development) as it it the default database used by Django framework. Good enough to build a Minimum Viable Product (MVP), will switch to MySQL or Postgres for production.
- **Environment Management**: Python-decouple library for environment variable management.

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

## Project Structure
```bash
Quizora/
├── .idea/
├── api/
│   ├── __pycache__/
│   ├── data/
│   │   ├── classyear_data.json
│   │   ├── gamesession_data.json
│   │   ├── progresstracking_data.json
│   │   ├── question_data.json
│   │   ├── quiz_data.json
│   │   └── user_data.json
│   ├── migrations/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   ├── 0002_auto_20241001_0101.py
│   │   ├── 0003_gamesession_correct_answers_count_and_more.py
│   │   ├── 0004_remove_gamesession_user_gamesession_student.py
│   │   ├── 0005_question_teacher.py
│   │   ├── 0006_load_dummy_data.py
│   │   └── 0007_delete_leaderboard.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── quizora/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .env
├── .gitignore
├── db.sqlite3
├── identifier.sqlite
├── LICENSE
├── manage.py
├── migration.bak
├── README.md
└── requirements.txt

```
