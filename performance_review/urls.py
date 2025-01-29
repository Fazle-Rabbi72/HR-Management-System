from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PerformanceReviewViewSet

router = DefaultRouter()
router.register(r'performance-reviews', PerformanceReviewViewSet, basename='performance-review')

urlpatterns = [
    path('', include(router.urls)),
]
