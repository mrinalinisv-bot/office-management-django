from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:pk>/toggle/', views.toggle_task, name='toggle_task'),
    path('tasks/<int:pk>/delete/', views.delete_task, name='delete_task'),
]
