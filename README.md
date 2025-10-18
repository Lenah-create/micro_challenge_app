Micro Challenge API
Overview
The Micro Challenge API is a backend system built with Django and Django REST Framework.
It allows users to create and manage micro-challenges, set reminders, log emotions, and track daily progress.
This project demonstrates backend development skills including model design, API creation, and database interaction.

Features
Challenges: Create, update, and view micro-challenges.
Reminders: Set daily reminders for challenges.
Emotion Logs: Record emotional states related to challenges.
Progress Tracking: Track completion and consistency for each challenge.

Tech Stack
Backend Framework: Django & Django REST Framework
Database: SQLite (default; can be switched to PostgreSQL for production)
Authentication: Django's built-in user authentication system
Deployment: Ready for deployment on Heroku or PythonAnywhere
API Endpoints
Endpoint	Method	Description
/api/challenges/	GET / POST	View or create a challenge
/api/challenges/<id>/	PUT / DELETE	Update or delete a challenge
/api/reminders/	GET / POST	List or create reminders
/api/reminders/<id>/	PUT / DELETE	Update or delete reminders
/api/emotions/	GET / POST	Log or view emotions
/api/progress/	GET / POST	Track user progress
Setup Instructions

1. Clone the Repository
git clone https://github.com/lenah-create/micro_challenge_app.git
cd micro_challenge_app