from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import TodoItem

# Get or create a unique session key for the user
def get_or_create_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

# View for displaying the ToDo list page
def todo_list(request):
    session_key = get_or_create_session_key(request)
    todos = TodoItem.objects.filter(session_key=session_key).order_by('-created_at')
    return render(request, 'todo_app/todo_list.html', {'todos':todos})

# View for adding a new ToDo item
def add_todo(request):
    session_key = get_or_create_session_key(request)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description','').strip()

        # Create page only if title exists
        if title:
            TodoItem.objects.create(title=title, description=description, session_key=session_key)

        # Return updated ToDo list
        todos = TodoItem.objects.filter(session_key=session_key).order_by('-created_at')
        return render(request, 'todo_app/todo_items.html', {'todos': todos})
    
    # Return empty response for GET requests
    return HttpResponse('')

# View for displaying edit form
def edit_todo_form(request, todo_id):
    session_key = get_or_create_session_key(request)
    todo = get_object_or_404(TodoItem, id=todo_id, session_key = session_key)
    return render(request, 'todo_app/edit_todo.html', {'todo': todo})

# View for updating a ToDo item
@csrf_exempt
def update_todo(request, todo_id):
    session_key = get_or_create_session_key(request)
    todo = get_object_or_404(TodoItem, id=todo_id, session_key=session_key)

    title = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()
    # Update ToDo if it has a title
    if title:
        todo.title = title
        todo.description = description
        todo.save()

        return redirect('todo_app:todo_list')

# View for toggling complete status of ToDo item
@csrf_exempt
def toggle_todo(request, todo_id):
    session_key = get_or_create_session_key(request)
    todo = get_object_or_404(TodoItem, id=todo_id, session_key=session_key)
    
    # Flip true to false or flase to true
    todo.completed = not todo.completed
    todo.save()

    # Return just the updated ToDo item
    return render(request, 'todo_app/todo_item.html', {'todo':todo})

# View to delete a ToDo item
@csrf_exempt
def delete_todo(request, todo_id):
    session_key = get_or_create_session_key(request)
    todo = get_object_or_404(TodoItem, id=todo_id, session_key=session_key)
    todo.delete()
    
    # Return empty response, item will be removed from DOM
    return HttpResponse('')