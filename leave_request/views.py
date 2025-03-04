from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Leave
from .serializers import LeaveSerializer
from django.utils.timezone import now
class LeaveViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LeaveSerializer

    def get_queryset(self):
        user = self.request.user
        today = now().date()
        approved_today = self.request.query_params.get('approved_today')
        if approved_today == 'true':
            if user.is_staff:
                return Leave.objects.filter(
                    status='Approved',
                    start_date__lte=today,  
                    end_date__gte=today     #
                )
            return Leave.objects.filter(
                employee=user.employee,
                status='Approved',
                start_date__lte=today,  
                end_date__gte=today     
            )
        #default show all leaves
        if user.is_staff:  
            return Leave.objects.all()
        return Leave.objects.filter(employee=user.employee)

    def perform_create(self, serializer):
     
        user = self.request.user
        if user.is_staff:  
            serializer.save()
        else:
            serializer.save(employee=user.employee)
