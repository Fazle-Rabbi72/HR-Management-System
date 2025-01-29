from django.shortcuts import render
from django.contrib.auth import authenticate,login

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Employee
from .serializers import EmployeeSerializer, EmployeeCreateSerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Department
from .serializers import DepartmentSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token  # Token-based auth
from .serializers import LoginSerializer
from user.models import User

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # Use the appropriate serializer based on the action
        if self.action == 'create':
            return EmployeeCreateSerializer
        return EmployeeSerializer


    def perform_update(self, serializer):
        # Handle updating user along with employee fields
        user_data = serializer.validated_data.pop('user', None)
        if user_data:
            password = user_data.pop('password', None)
            for attr, value in user_data.items():
                setattr(self.get_object().user, attr, value)
            if password:
                self.get_object().user.set_password(password)
            self.get_object().user.save()
        serializer.save()



class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Read-only for unauthenticated users





class LoginView(APIView):
    def post(self, request):
        # Serialize the login data (username or email and password)
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username_or_email = serializer.validated_data.get('username_or_email')
            password = serializer.validated_data.get('password')
            
            # Check if the username_or_email is a valid username or email
            user = None
            if '@' in username_or_email:
                # Try to find the user by email
                user = User.objects.filter(email=username_or_email).first()
            else:
                # Try to find the user by username
                user = User.objects.filter(username=username_or_email).first()

            if user:
                # Authenticate the user with the found username/email and password
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None and user.is_active:
                    # Create or fetch the auth token
                    token, _ = Token.objects.get_or_create(user=user)
                    
                    # Log the user in (create a session)
                    login(request, user)
                    
                    return Response({
                        'token': token.key,
                        'user_id': user.id,
                        'username': user.username,
                        'role': user.role
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid credentials or inactive user."}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
