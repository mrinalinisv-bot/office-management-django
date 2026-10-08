import datetime
from django.utils import timezone
from .models import Task

def oms_global_context(request):
    today = timezone.localdate() if timezone.is_aware(timezone.now()) else datetime.date.today()
    ten_days_later = today + datetime.timedelta(days=10)

    # Urgent & 10-day tasks for ticker alert
    alert_tasks = Task.objects.filter(
        is_completed=False,
        due_date__lte=ten_days_later
    ).order_by('due_date', '-priority')

    due_today_count = Task.objects.filter(is_completed=False, due_date=today).count()
    within_10_days_count = Task.objects.filter(
        is_completed=False,
        due_date__gte=today,
        due_date__lte=ten_days_later
    ).count()

    return {
        'scrolling_alerts': alert_tasks,
        'global_notification_count': alert_tasks.count(),
        'alert_10_days_count': within_10_days_count,
        'due_today_count': due_today_count,
        'current_today': today,
    }
