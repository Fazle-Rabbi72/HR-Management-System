from rest_framework import serializers
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
        user = User(**user_data)
        user.set_password(password)  # Hash password
        user.save()
        employee = Employee.objects.create(user=user, **validated_data)
        return employee
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']
        

class LoginSerializer(serializers.Serializer):
    username_or_email= serializers.CharField()  # Accepts either username or email
    password = serializers.CharField(write_only=True)
