from rest_framework.viewsets import ModelViewSet
from .models import Leave
from .serializers import LeaveSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class LeaveViewSet(ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    filter_backends = [DjangoFilterBackend ,filters.SearchFilter]  
    filterset_fields = ["employee"] 

    def get_queryset(self):
        if self.request.user.is_staff:
            # Admins can view all leave requests
            return Leave.objects.all()
        # Regular users can only view their own leave requests
        return Leave.objects.filter(employee=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the employee to the logged-in user
        serializer.save(employee=self.request.user)

    def update(self, request, *args, **kwargs):
        leave = self.get_object()
        if request.user.is_staff:
            # Admins can update the status
            leave.status = request.data.get('status', leave.status)
            leave.save()
            return Response({'message': 'Leave status updated successfully.'})
        # Regular users cannot update leave status
        return Response({'error': 'Permission denied.'}, status=403)
