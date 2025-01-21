from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now
from datetime import timedelta
from .models import Attendance
from .serializers import AttendanceSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    @action(detail=False, methods=['get'])
    def range(self, request):
        """
        Retrieve attendance records for a specified date range.
        Query parameters:
        - start_date (YYYY-MM-DD): Optional. Start date of the range.
        - end_date (YYYY-MM-DD): Optional. End date of the range.
        If not provided, defaults to the last 30 days.
        """
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Default to the last 30 days if no dates are provided
        if not start_date or not end_date:
            end_date = now().date()
            start_date = end_date - timedelta(days=30)

        try:
            # Convert string dates to proper date format
            start_date = start_date or (now().date() - timedelta(days=30))
            end_date = end_date or now().date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        # Filter attendance records within the date range
        attendances = Attendance.objects.filter(date__range=[start_date, end_date])

        # Calculate total working hours for the filtered records
        total_working_seconds = sum(
            (attendance.punch_out - attendance.punch_in).total_seconds()
            for attendance in attendances
            if attendance.punch_in and attendance.punch_out
        )

        # Convert total seconds to hours and minutes
        total_hours, total_remainder = divmod(total_working_seconds, 3600)
        total_minutes, _ = divmod(total_remainder, 60)

        serializer = self.get_serializer(attendances, many=True)

        return Response({
            "start_date": start_date,
            "end_date": end_date,
            "attendances": serializer.data,
            "total_working_hours": f"{int(total_hours)}h {int(total_minutes)}m"
        })
