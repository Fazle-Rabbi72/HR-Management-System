from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Leave
from .serializers import LeaveSerializer

class LeaveViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LeaveSerializer

    def get_queryset(self):
        
        user = self.request.user
        if user.is_staff:  
            return Leave.objects.all()
        return Leave.objects.filter(employee=user.employee)

    def perform_create(self, serializer):
     
      
        user = self.request.user
        if user.is_staff:  
            serializer.save()
        else:
            serializer.save(employee=user.employee)
