from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import TodoItem

# View for displaying the ToDo list page
def todo_list(request):
    todos = TodoItem.objects.all()
    return render(request, 'todo_app/todo_list.html', {'todos':todos})

# View for adding a new ToDo item
def add_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description','')

        # Create page only if title exists
        if title:
            TodoItem.objects.create(title=title, description=description)

        # Return updated ToDo list
        todos = TodoItem.objects.all()
        return render(request, 'todo_app/todo_items.html', {'todos': todos})
    
    # Return empty response for GET requests
    return HttpResponse('')

# View for toggling complete status of ToDo item
@csrf_exempt
def toggle_todo(request, todo_id):
    todo = get_object_or_404(TodoItem, id=todo_id)
    
    # Flip true to false or flase to true
    todo.completed = not todo.completed
    todo.save()

    # Return just the updated ToDo item
    return render(request, 'todo_app/todo_item.html', {'todo':todo})

# View to delete a ToDo item
@csrf_exempt
def delete_todo(request, todo_id):
    todo = get_object_or_404(TodoItem, id=todo_id)
    todo.delete()
    
    # Return empty response, item will be removed from DOM
    return HttpResponse('')