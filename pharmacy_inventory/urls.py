"""
URL configuration for pharmacy_inventory project.

Generated for the Pharmacy Inventory System & POS.
"""
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'Pharmacy Inventory System & POS'
admin.site.site_title = 'Pharmacy Inventory System & POS'
admin.site.index_title = 'Administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('inventory/', include('inventory.urls')),
    path('pos/', include('pos.urls')),
    path('', include('dashboard.urls')),
]
