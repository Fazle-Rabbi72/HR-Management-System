from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet

# Create a router and register the AttendanceViewSet
router = DefaultRouter()
router.register(r'attendance', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('', include(router.urls)),  # Include the router URLs
]
