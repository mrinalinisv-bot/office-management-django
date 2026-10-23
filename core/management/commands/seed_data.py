import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from core.models import Task

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds simple task reminder system with daily and 10-day alert tasks.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding task reminders...')

        # Create or update superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin / admin123'))

        today = timezone.localdate() if timezone.is_aware(timezone.now()) else datetime.date.today()

        if Task.objects.exists():
            self.stdout.write(self.style.WARNING(f'Database already contains {Task.objects.count()} tasks. Skipping seed to prevent data loss.'))
            return

        sample_tasks = [
            # 1. Daily tasks (Due Today)
            ("Submit Daily Operations Log", "Daily", 0, "Urgent", False, "Complete and sign end-of-day office dispatch register."),
            ("Team Morning Standup & Briefing", "Daily", 0, "High", False, "Review urgent action points with operations team."),
            ("Verify Petty Cash Expenses", "Bills & Utility", 0, "Medium", False, "Check daily physical receipts against accounts ledger."),

            # 2. Urgent / High tasks due nearly in 10 days
            ("Electricity Utility Bill Payment", "Bills & Utility", 2, "Urgent", False, "Pay electricity bill before late fee cutoff."),
            ("Renew Server Room AMC & Maintenance", "Official", 3, "High", False, "Annual maintenance contract deadline with vendor."),
            ("Comprehensive Insurance Policy Renewal", "Official", 5, "High", False, "Verify building coverage renewal documents."),
            ("Submit Monthly Tax & GST Return", "Bills & Utility", 7, "Urgent", False, "Reconcile invoices and finalize portal upload."),
            ("Fire Drill & Safety Equipment Inspection", "Official", 8, "High", False, "Test smoke alarms, extinguishers, and evacuation signs."),
            ("Quarterly Internet Leased Line Invoice", "Bills & Utility", 10, "Medium", False, "Clear Horizon ISP dedicated line charges."),

            # 3. Overdue task for alert testing
            ("Renew Software Antivirus License", "Official", -1, "Urgent", False, "Expired yesterday. Renew endpoint protection seats."),

            # 4. Later tasks (> 10 days)
            ("Vendor Quarterly Review Meeting", "Official", 15, "Medium", False, "Discuss catering and security vendor contracts."),
            ("Office Stationery Restock Requisition", "Personal", 20, "Low", False, "Check printer cartridges and registers."),

            # 5. Completed tasks
            ("Monthly Internet Bill Settlement", "Bills & Utility", -3, "High", True, "Paid via online bank transfer."),
            ("Fire Extinguisher Re-tagging", "Official", -5, "Medium", True, "Technician certified safety tags."),
        ]

        for title, cat, day_offset, prio, comp, desc in sample_tasks:
            Task.objects.create(
                title=title,
                category=cat,
                due_date=today + datetime.timedelta(days=day_offset),
                priority=prio,
                is_completed=comp,
                description=desc
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded task reminder data!'))
