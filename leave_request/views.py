from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Leave
from .serializers import LeaveSerializer

class LeaveViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Leave.objects.filter(employee=self.request.user.employee)

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user.employee)
