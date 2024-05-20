# Quiz App

This project is a Quiz App designed to offer users the ability to participate in quizzes across various categories. It provides a platform for users to engage in knowledge testing while also maintaining a scoreboard to track their progress.

## User Roles

### Admin
- Full control over quiz management, user data, and scoreboard.
- Add, update, and delete quizzes and categories.
- Monitor user activities and scores.

### Users
- Register, login, and participate in quizzes.
- View their scores and rankings in different categories.

## Key Features

1. **Quiz Management**: Admins can create, update, and delete quizzes categorized by different topics.
2. **User Authentication**: Secure registration and login system using JWT tokens.
3. **Scoreboard**: Tracks user scores and rankings in each quiz category.
4. **Category-wise Quizzes**: Users can choose quizzes based on different topics/categories.
5. **Quiz Participation**: Users can participate in quizzes, answer questions, and get immediate feedback.
6. **User Profiles**: Users can view their quiz history and scores.

## Setup

1. Clone repository.
2. Install dependencies (`pip install -r requirements.txt`).
3. Configure database settings in settings.py.
4. Run migrations (`python manage.py migrate`).
5. Create a superuser (`python manage.py createsuperuser`).
6. Run the application (`python manage.py runserver`).

## Tech Stack

- Backend: Django, Django REST Framework
- Frontend: HTML, JavaScript (Vue)
- Database: Django ORM

## Usage

1. As an admin, log in to the admin panel (`/admin`) to manage quizzes and categories.
2. Users can register and log in to participate in quizzes.
3. Users can view their scores and rankings in different quiz categories.
4. Admins can monitor user activities and scores through the admin dashboard.

## Contributors

- Viraj Joshi