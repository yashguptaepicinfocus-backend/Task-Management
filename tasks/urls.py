from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task-list'),
    path('my-tasks/', views.my_tasks, name='my-tasks'),
    path('create/', views.task_create, name='task-create'),
    path('<int:pk>/', views.task_detail, name='task-detail'),
    path('<int:pk>/update/', views.task_update, name='task-update'),
    path('<int:pk>/delete/', views.task_delete, name='task-delete'),
    path('<int:pk>/status/', views.task_update_status, name='task-update-status'),
]
