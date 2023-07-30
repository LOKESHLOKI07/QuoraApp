from django.contrib import admin
from django.urls import path
from quoraapp import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('home', views.home, name='home'),
    path('post_question/', views.post_question, name='post_question'),
    path('post_answer/<int:question_id>/', views.post_answer, name='post_answer'),
    path('like_answer/<int:answer_id>/', views.like_answer, name='like_answer'),
    path('logout/', views.user_logout, name='logout'),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.user_registration, name='register'),
    path('question_detail/<int:question_id>/', views.question_detail, name='question_detail'),
    path('question/<int:question_id>/reply/', views.reply_question, name='reply_question'),
    path('like_question/<int:question_id>/', views.like_question, name='like_question'),


]