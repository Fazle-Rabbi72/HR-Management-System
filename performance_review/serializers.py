from rest_framework import serializers
from .models import PerformanceReview

class PerformanceReviewSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.username', read_only=True)
    reviewer_name = serializers.CharField(source='reviewer.username', read_only=True)

    class Meta:
        model = PerformanceReview
        fields = [
            'id', 
            'employee', 
            'employee_name', 
            'reviewer', 
            'reviewer_name',
            'review_date', 
            'period_start', 
            'period_end', 
            'feedback', 
            'rating'
        ]
        read_only_fields = ['review_date']
