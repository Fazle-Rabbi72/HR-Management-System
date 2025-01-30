from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Attendance
from .serializers import AttendanceSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    @action(detail=False, methods=['get'])
    def by_employee(self, request):
        """
        Retrieve attendance records for a specific employee.
        Query parameter:
        - employee_id (required): Employee ID to filter attendance.
        """
        employee_id = request.query_params.get('employee_id')

        if not employee_id:
            return Response({"error": "employee_id is required."}, status=400)

        attendances = Attendance.objects.filter(employee_id=employee_id)
        serializer = self.get_serializer(attendances, many=True)

        return Response(serializer.data)
