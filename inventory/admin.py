from django.contrib import admin

from .models import Category, Medicine, MedicineBarcode, Supplier


class MedicineBarcodeInline(admin.TabularInline):
    model = MedicineBarcode
    extra = 1


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'generic_name', 'category', 'supplier', 'strength', 'selling_price')
    search_fields = ('brand_name', 'generic_name')
    list_filter = ('category', 'supplier')
    inlines = [MedicineBarcodeInline]


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'contact_number', 'lead_time_days', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'contact_person', 'contact_number')


@admin.register(MedicineBarcode)
class MedicineBarcodeAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'medicine', 'created_at')
    search_fields = ('barcode', 'medicine__brand_name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

