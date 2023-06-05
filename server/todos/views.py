from rest_framework.decorators import api_view
from .models import Todo
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.response import Response
from .serializers.todo import TodoListSerializer, TodoSerializer
from rest_framework import status


@api_view(['GET', 'POST'])
def todo_list(request):
    if request.method == 'GET':
        todos = get_list_or_404(Todo)
        serializer = TodoListSerializer(todos, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH', 'DELETE'])
def todo_detail(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk)
    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        todo.delete()
        data = {
            'delete': f'review {todo_pk} is deleted'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)
