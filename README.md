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
- `accounts/` - Log in/out, roles, audit logs, settings (`/accounts/`)
- `pos/` - Point-of-sale app (`/pos/`)
- Admin site: `/admin/` (create a superuser with `python manage.py createsuperuser`)

## Pages

| Page | URL |
| --- | --- |
| Dashboard | `/` |
| Medicines | `/inventory/medicines/` |
| Categories | `/inventory/categories/` (add/edit/delete for admins and pharmacists) |
| Suppliers | `/inventory/suppliers/` (add/edit/delete for admins and pharmacists) |
| Stocks | `/inventory/stocks/` |
| Expiry Dates | `/inventory/expiry-dates/` |
| Alerts | `/inventory/alerts/` |
| Roles | `/accounts/roles/` |
| Audit Logs | `/accounts/audit-logs/` |
| Accounts & Settings | `/accounts/settings/` |

All pages above require authentication. Anonymous visitors are redirected to `/accounts/login/?next=<page>`. Only the login page is public; the Django admin keeps its own login at `/admin/login/`.

There is no public signup. Administrators create users in `/admin/` and can assign them to groups such as **Pharmacist** and **Cashier**. The groups `Administrator`, `Pharmacist`, and `Cashier` are created automatically by a migration.

## Medicines

- Category and Supplier are optional. Leave them blank to save the medicine, then fill them in later while editing — or type a new name in **Add New Category** / **Add New Supplier** to create one on the spot.
- Administrators (superusers / `Administrator` group) and users in the `Pharmacist` group can add, edit, and delete medicines. Cashiers cannot.
- Edit at `/inventory/medicines/<id>/edit/` and delete at `/inventory/medicines/<id>/delete/`.
- **Register Medicine Barcode** is optional — save the medicine first and add barcodes later by editing it. A medicine can have several barcodes; type or scan one per line. Removing a barcode on edit also frees it for reuse.
- The same field supports manual typing, a USB scanner in HID/keyboard mode, and **Scan with Camera** (1D/2D) via the browser's `html5-qrcode` library. Camera access requires `localhost` or HTTPS. No extra Python package is needed.
- Barcode lookup for POS: `/inventory/barcode-lookup/?barcode=<code>` returns JSON medicine details (requires login).
