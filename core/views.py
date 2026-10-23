import calendar
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Task
from .forms import TaskForm

def dashboard(request):
    today = timezone.localdate() if timezone.is_aware(timezone.now()) else datetime.date.today()
    ten_days_later = today + datetime.timedelta(days=10)

    filter_type = request.GET.get('filter', 'all')
    search_q = request.GET.get('q', '').strip()

    # Base tasks queryset
    base_tasks = Task.objects.all()
    if search_q:
        base_tasks = base_tasks.filter(title__icontains=search_q)

    # Filtered tasks for main view
    if filter_type == 'today':
        tasks = base_tasks.filter(is_completed=False, due_date=today)
    elif filter_type == '10days':
        tasks = base_tasks.filter(is_completed=False, due_date__gte=today, due_date__lte=ten_days_later)
    elif filter_type == 'overdue':
        tasks = base_tasks.filter(is_completed=False, due_date__lt=today)
    elif filter_type == 'completed':
        tasks = base_tasks.filter(is_completed=True)
    else:
        tasks = base_tasks

    # Specific alert lists:
    # 1. Nearly 10 days important tasks
    ten_day_alerts = Task.objects.filter(
        is_completed=False,
        due_date__gte=today,
        due_date__lte=ten_days_later
    ).order_by('due_date', '-priority')

    # 2. Daily tasks (Due today)
    daily_tasks = Task.objects.filter(
        is_completed=False,
        due_date=today
    ).order_by('-priority')

    # 3. Overdue alerts
    overdue_tasks = Task.objects.filter(
        is_completed=False,
        due_date__lt=today
    ).order_by('due_date')

    # Summary Metrics
    total_count = Task.objects.count()
    due_today_count = Task.objects.filter(is_completed=False, due_date=today).count()
    in_10_days_count = ten_day_alerts.count()
    completed_count = Task.objects.filter(is_completed=True).count()

    form = TaskForm()

    context = {
        'tasks': tasks,
        'daily_tasks': daily_tasks,
        'ten_day_alerts': ten_day_alerts,
        'overdue_tasks': overdue_tasks,
        'total_count': total_count,
        'due_today_count': due_today_count,
        'in_10_days_count': in_10_days_count,
        'completed_count': completed_count,
        'filter_type': filter_type,
        'search_q': search_q,
        'form': form,
        'active_tab': 'dashboard',
    }
    return render(request, 'dashboard.html', context)


def calendar_view(request):
    today = timezone.localdate() if timezone.is_aware(timezone.now()) else datetime.date.today()
    try:
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))
        if month < 1 or month > 12:
            month = today.month
    except (ValueError, TypeError):
        year = today.year
        month = today.month

    # Navigation: Prev and Next month
    if month == 1:
        prev_year = year - 1
        prev_month = 12
    else:
        prev_year = year
        prev_month = month - 1

    if month == 12:
        next_year = year + 1
        next_month = 1
    else:
        next_year = year
        next_month = month + 1

    # Fetch all tasks in this month
    month_tasks = Task.objects.filter(
        due_date__year=year,
        due_date__month=month
    ).order_by('due_date', '-priority')

    tasks_by_date = {}
    for task in month_tasks:
        tasks_by_date.setdefault(task.due_date, []).append(task)

    # Calendar generation (Sunday = first day of week)
    cal = calendar.Calendar(firstweekday=6)
    month_weeks = cal.monthdatescalendar(year, month)

    calendar_weeks = []
    for week in month_weeks:
        week_days = []
        for day in week:
            day_tasks = tasks_by_date.get(day, [])
            week_days.append({
                'date': day,
                'day_num': day.day,
                'is_current_month': (day.month == month),
                'is_today': (day == today),
                'tasks': day_tasks,
                'has_tasks': len(day_tasks) > 0,
            })
        calendar_weeks.append(week_days)

    form = TaskForm()

    context = {
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'calendar_weeks': calendar_weeks,
        'month_tasks': month_tasks,
        'total_month_tasks': month_tasks.count(),
        'form': form,
        'active_tab': 'calendar',
    }
    return render(request, 'calendar.html', context)


@require_POST
def create_task(request):
    form = TaskForm(request.POST)
    if form.is_valid():
        task = form.save()
        messages.success(request, f'Task "{task.title}" created with {task.priority} priority!')
    else:
        err_list = []
        for field, errors in form.errors.items():
            err_list.append(f"{field}: {', '.join(errors)}")
        err_str = "; ".join(err_list) if err_list else "Invalid form submission"
        messages.error(request, f'Failed to add task: {err_str}')
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)


@require_POST
def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = not task.is_completed
    task.save()
    if task.is_completed:
        messages.success(request, f'✓ Completed "{task.title}"!')
    else:
        messages.info(request, f'Reopened "{task.title}".')
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)


@require_POST
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    title = task.title
    task.delete()
    messages.warning(request, f'Task "{title}" removed.')
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)


def db_status(request):
    from django.http import JsonResponse
    from django.db import connection
    return JsonResponse({
        'vendor': connection.vendor,
        'task_count': Task.objects.count(),
        'version': 'v2-neon',
    })
