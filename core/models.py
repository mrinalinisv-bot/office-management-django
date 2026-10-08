from django.db import models
from django.utils import timezone
from datetime import date

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Urgent', 'Urgent'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    CATEGORY_CHOICES = [
        ('Daily', 'Daily Task'),
        ('Bills & Utility', 'Bills & Utility'),
        ('Official', 'Official / Admin'),
        ('Personal', 'Personal'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Daily')
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(default=timezone.now)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['is_completed', 'due_date', '-priority']

    def __str__(self):
        return f"{self.title} - Due {self.due_date} [{self.priority}]"

    @property
    def days_remaining(self):
        today = timezone.localdate() if timezone.is_aware(timezone.now()) else date.today()
        return (self.due_date - today).days

    @property
    def is_due_today(self):
        return self.days_remaining == 0

    @property
    def is_overdue(self):
        return self.days_remaining < 0

    @property
    def is_due_within_10_days(self):
        return 0 <= self.days_remaining <= 10

    @property
    def status_label(self):
        if self.is_completed:
            return "Completed"
        if self.is_overdue:
            days = abs(self.days_remaining)
            return f"Overdue ({days}d)"
        if self.is_due_today:
            return "Due Today"
        if self.days_remaining == 1:
            return "Due Tomorrow"
        return f"Due in {self.days_remaining} Days"

    @property
    def day_number(self):
        return self.due_date.strftime('%d')

    @property
    def month_short(self):
        return self.due_date.strftime('%b').upper()
