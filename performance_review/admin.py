from django.contrib import admin
from .models import PerformanceReview

@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('employee', 'reviewer', 'review_date', 'rating')
    list_filter = ('review_date', 'rating')
    search_fields = ('employee__username', 'reviewer__username')
