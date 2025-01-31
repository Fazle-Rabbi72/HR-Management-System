from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from .models import User, Employee, Department

class EmployeeSerializer(serializers.ModelSerializer):
    # Nested User Data (username, email, role, password)
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, source='user.role')
    department_name = serializers.ReadOnlyField(source='department.name')
    
    class Meta:
        model = Employee
        fields = [
            'id',
            'username',
            'role',
            'first_name',
            'last_name',
            'email',
            'department',
            'department_name',
            'designation',
            'date_of_joining',
            'phone',
            'address',
            'profile_image',
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            # Update the user data (including password if provided)
            password = user_data.pop('password', None)
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            if password:
                instance.user.set_password(password)
            instance.user.save()

        # Update employee-specific data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class EmployeeCreateSerializer(serializers.ModelSerializer):
    # Handle password creation for new employees
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, source='user.role')
    password = serializers.CharField(write_only=True)
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = Employee
        fields = [
            'id',
            'username',
            'role',
            'first_name',
            'last_name',
            'email',
            'department',
            'designation',
            'date_of_joining',
            'phone',
            'address',
            'profile_image',
            'password',
        ]
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = validated_data.pop('password')

        # Create User
        user = User(**user_data)
        user.set_password(password)  # Hash password
        user.save()

        # Create Employee
        employee = Employee.objects.create(user=user, **validated_data)

        # Send Email Notification with username, email, and password
        self.send_employee_email(employee, password)

        return employee

    def send_employee_email(self, employee, password):
        subject = "Your Job Confirmation at Our Company"
        message = f"""
        Dear {employee.user.first_name} {employee.user.last_name},

        Congratulations! You have been successfully appointed as **{employee.designation}** in the **{employee.department.name}** department. 

        Your role in our system: **{employee.user.get_role_display()}**.
        Your joining date: **{employee.date_of_joining}**.

        Here are your login details:
        🔹 **Username**: {employee.user.username}
        🔹 **Email**: {employee.user.email}
        🔹 **Password**: {password}

        Please log in to your account and change your password as soon as possible.

        Login URL: http://127.0.0.1:8000/login/

        Regards,  
        HR Team  
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Ensure this is set in settings.py
            [employee.user.email],
            fail_silently=False,
        )
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']
        

class LoginSerializer(serializers.Serializer):
    username_or_email= serializers.CharField()  # Accepts either username or email
    password = serializers.CharField(write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "New password and confirm password do not match."})
        return data
    
class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()
    
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data