# Pharmacy Inventory System & POS

A Django project for managing pharmacy inventory and point-of-sale operations.

## Setup

```powershell
# Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies (first time only)
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Run the development server
python manage.py runserver
```

## Structure

- `pharmacy_inventory/` - Django project settings and root URLs
- `frontend/` - Shared templates (`templates/`) and static assets (`static/css`, `static/js`, `static/images`)
- `accounts/` - User accounts: sign up, log in/out, profile (`/accounts/`)
- `inventory/` - Inventory management app (`/`)
- `pos/` - Point-of-sale app (`/pos/`)
- Admin site: `/admin/` (create a superuser with `python manage.py createsuperuser`)
