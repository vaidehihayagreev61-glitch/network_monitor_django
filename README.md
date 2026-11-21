# Network Monitoring System (Django)

A beginner-friendly Django project for recording devices and checking connectivity
to devices you own or are authorized to monitor. It does not scan networks or
discover unknown devices.

## Requirements
- Python 3.10+
- Internet connection for the Bootstrap and Chart.js CDN assets (optional; the
  app still works without charts/styling if the CDNs are unavailable).

## Windows setup (VS Code terminal)
```bash
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ and sign in using the superuser account.
Django admin: http://127.0.0.1:8000/admin/

## macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Main features
- Admin login and logout
- Dashboard summary
- Add, edit, view and delete monitored devices
- Manually check connectivity to a saved device
- Monitoring history and a simple chart
- Django admin interface

## Important network-use note
Only add devices and IP addresses that belong to you or that you have explicit
permission to monitor. Checks are individual ping requests to saved addresses;
there is no network-wide scanning.

## Project structure
```
network_monitor/
├── manage.py
├── requirements.txt
├── README.md
├── network_monitor/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── monitoring/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── urls.py
    ├── views.py
    └── templates/monitoring/
        ├── base.html
        ├── login.html
        ├── dashboard.html
        ├── device_list.html
        ├── device_form.html
        ├── device_confirm_delete.html
        └── reports.html
```
