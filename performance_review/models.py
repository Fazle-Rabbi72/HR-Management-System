from django.db import models


from user.models import User

class PerformanceReview(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="performance_reviews")
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="given_reviews")
    review_date = models.DateField(auto_now_add=True)
    period_start = models.DateField()
    period_end = models.DateField()
    feedback = models.TextField()
    rating = models.DecimalField(max_digits=4, decimal_places=2, help_text="Rating out of 10")
    
    def __str__(self):
        return f"{self.employee.username} - {self.review_date}"

    class Meta:
        ordering = ["-review_date"]
