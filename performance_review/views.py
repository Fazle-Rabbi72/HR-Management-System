from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import PerformanceReview
from .serializers import PerformanceReviewSerializer

class PerformanceReviewViewSet(ModelViewSet):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Allow employees to view their own reviews
        if not self.request.user.is_staff:
            return PerformanceReview.objects.filter(employee=self.request.user)
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
