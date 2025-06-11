from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
urlpatterns = [
    path('',views.index, name="index" ),
    path('topics/', views.topics, name="topics"),
    path('topic/<int:pk>/', views.topic, name='topic'),
    path('new_topic', views.new_topic, name= "new_topic"),
    path('new_entry/<int:pk>/', views.new_entry, name="new_entry"),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name="edit_entry"),
    path('login/', LoginView.as_view(), {'template_name': 'login.html'}, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register', views.register, name="register"),
]