# Task Management System - Django Based

A comprehensive web-based Task Management System built with Django, featuring hierarchical task assignment within departments, role-based access control, and structured workflow management.

## Features

### User Roles
- **Admin**: Full access across all departments
- **Manager**: Can assign tasks within their department only
- **Employee**: Can view and update their assigned tasks

### Core Functionality
- Department-based hierarchy
- Task creation with assignment and due dates
- Task status tracking (Pending, In Progress, Completed)
- Role-based permissions enforcement
- Department-wise task filtering
- Dashboard with statistics
- Task comments system
- Overdue task detection

## Technology Stack

- **Backend**: Django 4.2+
- **Database**: PostgreSQL
- **Authentication**: Django Auth System (Custom User Model)
- **Frontend**: Bootstrap 5, HTML5
- **Icons**: Bootstrap Icons

## Project Structure

```
task_management/
├── accounts/               # User authentication and management
│   ├── models.py          # Custom User model, Department model
│   ├── views.py           # Login, logout, dashboard views
│   ├── forms.py           # Authentication forms
│   ├── admin.py           # Admin configurations
│   └── templates/         # HTML templates
├── tasks/                 # Task management
│   ├── models.py          # Task and TaskComment models
│   ├── views.py           # CRUD views with role-based permissions
│   ├── forms.py           # Task forms with validation
│   ├── admin.py           # Task admin configurations
│   └── templates/         # HTML templates
├── task_management/       # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/             # Base templates
│   └── base.html
├── requirements.txt       # Python dependencies
└── manage.py
```

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd task-management

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Database Setup

1. Create a PostgreSQL database:
```sql
CREATE DATABASE task_management;
```

2. Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=task_management
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

### Step 3: Database Migration

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Superuser

```bash
python manage.py createsuperuser
```

### Step 5: Run Development Server

```bash
python manage.py runserver
```

Access the application at: http://127.0.0.1:8000

## Usage

### Initial Setup

1. Login to Django Admin at `/admin/`
2. Create departments (e.g., IT, HR, Sales, Marketing)
3. Create users and assign them to departments with appropriate roles:
   - Admin: Full system access
   - Manager: Department-level task management
   - Employee: Task execution and updates

### Role-Based Permissions

#### Admin
- View all tasks across all departments
- Create/update/delete any task
- Assign tasks to any user
- Access full dashboard statistics

#### Manager
- View tasks within their department only
- Create tasks for their department
- Assign tasks to employees in their department
- Cannot assign cross-department tasks

#### Employee
- View only their assigned tasks
- Update task status
- Add comments to tasks
- Cannot create or assign tasks

### Task Workflow

1. **Create Task**: Managers/Admins create tasks with title, description, department, assignee, priority, and due date
2. **Assignment**: Task is assigned to an employee within the same department
3. **Status Updates**: Employees update status from Pending → In Progress → Completed
4. **Comments**: Team members can add comments for collaboration
5. **Monitoring**: Managers track progress through the dashboard

## API Endpoints (URL Routes)

### Authentication
- `/login/` - User login
- `/logout/` - User logout

### Dashboard
- `/` - Dashboard (role-based view)
- `/profile/` - User profile

### Tasks
- `/tasks/` - Task list with filters
- `/tasks/my-tasks/` - Employee's assigned tasks
- `/tasks/create/` - Create new task (Managers/Admins only)
- `/tasks/<id>/` - Task detail view
- `/tasks/<id>/update/` - Update task (Managers/Admins only)
- `/tasks/<id>/delete/` - Delete task (Managers/Admins only)
- `/tasks/<id>/status/` - Update task status

### Admin
- `/admin/` - Django Admin interface

## Security Features

- CSRF protection on all forms
- Role-based access control (RBAC)
- Department-level data isolation
- Permission validation on all views
- Secure password handling
- Session management

## Deployment

### Production Settings

1. Set `DEBUG=False` in `.env`
2. Update `ALLOWED_HOSTS` with your domain
3. Configure production database
4. Set up static files:
```bash
python manage.py collectstatic
```

5. Use a production WSGI server (Gunicorn, uWSGI)
6. Configure reverse proxy (Nginx, Apache)

### Docker Deployment

A `Dockerfile` and `docker-compose.yml` can be added for containerized deployment.

## Testing

Run the test suite:
```bash
python manage.py test
```

## Future Enhancements

- [ ] Email notifications for task assignments
- [ ] File attachments for tasks
- [ ] Audit logs
- [ ] REST API with Django REST Framework
- [ ] Mobile application
- [ ] Real-time notifications
- [ ] Advanced reporting and analytics
- [ ] Multi-company SaaS model

## License

This project is proprietary and confidential.

## Support

For support and queries, please contact the development team.

---

**Note**: This is a Phase 1 implementation focusing on core functionality. Phase 2-4 features will be implemented in future iterations.
