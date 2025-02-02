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
        # Check if the user is an admin or staff
        if self.request.user.is_staff:
            # Admin can view all leave requests
            return Leave.objects.all()

        # Check if the user is authenticated and is an employee
        if self.request.user.is_authenticated:
            # Regular employees can only view their own leave requests
            return Leave.objects.filter(employee=self.request.user)

        # If not authenticated, return empty queryset
        return Leave.objects.none()

    def perform_create(self, serializer):
        # Check if the user is authenticated
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to create a leave request.")

        # Automatically set the employee to the logged-in user
        serializer.save(employee=self.request.user)

    def update(self, request, *args, **kwargs):
        leave = self.get_object()

        # Check if the user is staff (admin)
        if request.user.is_staff:
            # Admins can update the leave status
            leave.status = request.data.get('status', leave.status)
            leave.save()
            return Response({'message': 'Leave status updated successfully.'})

        # Employees cannot update their leave status
        return Response({'error': 'Permission denied.'}, status=403)
