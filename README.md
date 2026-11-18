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
- `dashboard/` - Dashboard page (`/`)
- `inventory/` - Medicines, categories, suppliers, stocks, expiry dates, alerts (`/inventory/`)
- `accounts/` - Sign up, log in/out, profile, roles, audit logs, settings (`/accounts/`)
- `pos/` - Point-of-sale app (`/pos/`)
- Admin site: `/admin/` (create a superuser with `python manage.py createsuperuser`)

## Pages

| Page | URL |
| --- | --- |
| Dashboard | `/` |
| Medicines | `/inventory/medicines/` |
| Categories | `/inventory/categories/` |
| Suppliers | `/inventory/suppliers/` |
| Stocks | `/inventory/stocks/` |
| Expiry Dates | `/inventory/expiry-dates/` |
| Alerts | `/inventory/alerts/` |
| Roles | `/accounts/roles/` |
| Audit Logs | `/accounts/audit-logs/` |
| Accounts & Settings | `/accounts/settings/` |
