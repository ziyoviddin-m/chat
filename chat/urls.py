from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='chat/login.html'), name='login'),
    path('users/', views.users, name='users'),
    path('logout/', views.logout, name='logout'),
    path('chat/<int:chat_id>/', views.chat, name='chat'),

]