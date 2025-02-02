from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.core.mail import send_mail
import random
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Employee
from .serializers import EmployeeSerializer, EmployeeCreateSerializer,ChangePasswordSerializer,ResetPasswordRequestSerializer,ResetPasswordSerializer,VerifyOTPSerializer,LoginSerializer,DepartmentSerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Department

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token  # Token-based auth

from user.models import User

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    

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
    # permission_classes = [IsAuthenticatedOrReadOnly]  # Read-only for unauthenticated users





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
                        'id': user.id if user.role == 'admin' else None,
                        'user_id': user.employee.id if hasattr(user, 'employee') and user.role == 'employee' else None,
                        'username': user.username,
                        'role': user.role,
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({"error": "Invalid credentials or inactive user."}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer=ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user=request.user
            
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordRequestView(APIView):
    def post(self, request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            
            if not user:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

            otp = random.randint(100000, 999999)
            user.otp = otp
            user.otp_created_at = now()
            user.save()

           
            send_mail(
                "Password Reset OTP",
                f"Your OTP for password reset is: {otp}",
                "noreply@yourdomain.com",
                [email],
                fail_silently=False,
            )

            return Response({"message": "OTP sent to email."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']

            user = User.objects.filter(email=email, otp=otp).first()

            if not user:
                return Response({"error": "Invalid OTP or email."}, status=status.HTTP_400_BAD_REQUEST)

            
            return Response({"message": "OTP verified. You can reset your password now."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']

            user = User.objects.filter(email=email, otp=otp).first()

            if not user:
                return Response({"error": "Invalid OTP or email."}, status=status.HTTP_400_BAD_REQUEST)

        
            user.set_password(new_password)
            user.otp = None  
            user.save()

            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)