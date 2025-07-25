from django.urls import path
from . import views

app_name = 'todo_app'

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('add/', views.add_todo, name='add_todo'),
    path('toggle/<int:todo_id>/', views.toggle_todo, name='toggle_todo'),
    path('update/<int:todo_id>/',views.update_todo, name='update_todo'),
    path('edit/<int:todo_id>/', views.edit_todo_form, name='edit_todo_form'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
]