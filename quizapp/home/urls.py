from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

#all paths are mentioned here
urlpatterns = [
    path('', views.home, name="home"),
    path('api/get_quiz/', login_required(views.get_quiz), name="get_quiz"),
    path('quiz/', login_required(views.quiz), name="quiz"),
    path('score_feedback/', login_required(views.score_feedback), name='score_feedback'),
    path('signup/', views.signup, name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('save_user_score/', views.save_user_score, name='save_quiz_score'),
    path('user_dashboard/', login_required(views.user_dashboard), name='user_dashboard'),
    path('category_leaderboard/<str:category_name>/', views.category_leaderboard, name='category_leaderboard'),
    path('submit_quiz/', views.submit_quiz, name='submit_quiz'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
