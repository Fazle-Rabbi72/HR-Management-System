from rest_framework import serializers
from .models import User, Employee


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


class EmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username') 
    first_name = serializers.CharField(source='user.first_name') 
    last_name = serializers.CharField(source='user.last_name') 
    email = serializers.EmailField(source='user.email') 
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, source='user.role')  

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
            'profile_image_url',
        ]


class EmployeeCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')  
    first_name = serializers.CharField(source='user.first_name') 
    last_name = serializers.CharField(source='user.last_name') 
    email = serializers.EmailField(source='user.email') 
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, source='user.role')  

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
            'profile_image_url',
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        employee = Employee.objects.create(user=user, **validated_data)
        return employee
