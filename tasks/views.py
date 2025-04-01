from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework import permissions
from .models import Task
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from tasks.serializers import RegisterSerializer
from .serializers import TaskSerializer


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class TaskAssignView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Check if user is Team Lead
        if request.user.role != 'team_lead':
            return Response({"error": "Only Team Leads can assign tasks."}, status=403)

        task = Task.objects.create(
            title=request.data.get('title'),
            assigned_to=request.data.get('assigned_to'),
            assigned_by=request.user,
            status='pending'
        )

        serializer = TaskSerializer(task)
        return Response(serializer.data)