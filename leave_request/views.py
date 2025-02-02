from rest_framework.viewsets import ModelViewSet
from .models import Leave
from .serializers import LeaveSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

class LeaveViewSet(ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["employee"]

    def get_queryset(self):
        # Return all leave requests for everyone
        return Leave.objects.all()

    def perform_create(self, serializer):
        # Automatically set the employee to the logged-in user for the leave request
        serializer.save(employee=self.request.user)

    def update(self, request, *args, **kwargs):
        leave = self.get_object()

        # Allow any authenticated user to update the leave status if they are an admin
        if request.user.is_staff:
            leave.status = request.data.get('status', leave.status)
            leave.save()
            return Response({'message': 'Leave status updated successfully.'})

        # Non-admin users cannot update leave status
        return Response({'error': 'Permission denied.'}, status=403)
