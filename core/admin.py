from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'due_date', 'priority', 'is_completed', 'status_label')
    list_filter = ('is_completed', 'priority', 'category', 'due_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'due_date'
