# Office Task & Reminder Alert System (OMS)

A clean, focused Django application with PostgreSQL database connectivity designed for daily task tracking and priority-based 10-day alert reminders.

---

## Key Features

1. **Scrolling Upcoming Tasks Alert Ticker**:
   - A live, animated ticker banner at the top displaying urgent and important tasks due in the next 10 days.
   - Highlights task priority (`Urgent`, `High`, `Medium`) and real-time countdown tags (`Due Today`, `Due Tomorrow`, `Due in X Days`).
   - Pauses on hover for comfortable reading.

2. **Daily Task Tracker**:
   - Dedicated "Today's Daily Tasks" section for immediate daily routine items.
   - One-click completion checkbox toggle with instant visual strike-through.

3. **10-Day Important Alerts**:
   - Highlight panel for upcoming high-priority deadlines (bills, statutory filings, renewals, inspections).
   - Priority-coded badges:
     - 🚨 **Urgent**
     - ⚡ **High**
     - 🔹 **Medium**
     - ▫️ **Low**

4. **Task Creation with Priority**:
   - Quick modal form to add tasks with title, category, priority, due date, and notes.

5. **Filterable Task View**:
   - Filter by: `All`, `⚡ Next 10 Days`, `📅 Due Today`, `⚠️ Overdue`, `✓ Completed`.
   - Real-time text search.

6. **PostgreSQL Database Connection**:
   - Backed by PostgreSQL (`oms_db`) using `psycopg2-binary`.
   - Pre-configured admin interface at `/admin/` (User: `admin` / Password: `admin123`).

---

## Project Structure

```
office_management_system/
├── core/
│   ├── management/commands/seed_data.py  # Seed initial sample data
│   ├── admin.py                          # Admin panel configuration
│   ├── context_processors.py             # Feeds live scrolling ticker data
│   ├── forms.py                          # TaskForm with priority choices
│   ├── models.py                         # Clean Task model with countdown helpers
│   ├── urls.py                           # Application routes
│   └── views.py                          # Dashboard, create, toggle, delete views
├── oms_project/
│   ├── settings.py                       # PostgreSQL DATABASES config
│   ├── urls.py                           # Root URL configuration
│   └── wsgi.py
├── static/
│   └── css/style.css                     # Marquee ticker & dashboard styling
├── templates/
│   ├── base.html                         # Layout with scrolling marquee ticker
│   └── dashboard.html                    # Daily tasks, 10-day alerts & tracker
├── manage.py
└── requirements.txt
```

---

## Quick Start Instructions

### 1. Database Setup
PostgreSQL database `oms_db` is configured in `settings.py`:
- **DB Name**: `oms_db`
- **User**: `postgres`
- **Password**: `postgres`
- **Host**: `localhost`
- **Port**: `5432`

### 2. Run Database Migrations (already completed)
```bash
python manage.py makemigrations core
python manage.py migrate
```

### 3. Seed Realistic Sample Data
```bash
python manage.py seed_data
```

### 4. Start the Development Server
```bash
python manage.py runserver
```
Open **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.
Open **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)** for the administrative database interface.
