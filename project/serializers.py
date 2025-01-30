from rest_framework import serializers
from .models import Project, Client,Team
from user.serializers import EmployeeSerializer

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    leader = EmployeeSerializer() 
    members = EmployeeSerializer(many=True)  

    class Meta:
        model = Team
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True) 

    class Meta:
        model = Project
        fields = ['id', 'name','client','department', 'description', 'price', 'start_date', 'end_date','status','team']
