from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm, MedicineForm, SupplierForm
from .models import Category, Medicine, MedicineBarcode, Supplier
from .permissions import can_manage_inventory


PLACEHOLDER_PAGES = {
    'stocks': ('inventory/stocks.html', 'Stocks', 'Track stock levels and replenishments.'),
    'expiry_dates': ('inventory/expiry-dates.html', 'Expiry Dates', 'Monitor batch expiry dates and approaching expiries.'),
    'alerts': ('inventory/alerts.html', 'Alerts', 'Low stock, expired batch, and other system alerts.'),
}


def _placeholder(request, page):
    template, title, description = PLACEHOLDER_PAGES[page]
    return render(request, template, {'page_title': title, 'description': description})


def _deny_if_not_manager(request, redirect_to='medicines'):
    if not can_manage_inventory(request.user):
        messages.error(request, 'Only administrators and pharmacists can manage inventory records.')
        return redirect(redirect_to)
    return None


def _save_medicine(form):
    new_category = form.cleaned_data.get('new_category', '').strip()
    new_supplier = form.cleaned_data.get('new_supplier', '').strip()

    medicine = form.save(commit=False)
    if new_category:
        medicine.category, _ = Category.objects.get_or_create(name=new_category)
    if new_supplier:
        medicine.supplier, _ = Supplier.objects.get_or_create(name=new_supplier)
    medicine.save()

    barcodes = form.cleaned_data.get('barcodes') or []
    if not barcodes:
        return medicine

    existing = set(medicine.barcodes.values_list('barcode', flat=True))
    medicine.barcodes.filter(barcode__in=existing - set(barcodes)).delete()
    for barcode in barcodes:
        if barcode not in existing:
            MedicineBarcode.objects.create(medicine=medicine, barcode=barcode)

    return medicine


@login_required
def medicines(request):
    medicines = (
        Medicine.objects
        .select_related('category', 'supplier')
        .prefetch_related('barcodes')
    )

    selected_category = None
    category_id = request.GET.get('category')
    if category_id and category_id.isdigit():
        selected_category = Category.objects.filter(pk=category_id).first()
    if selected_category:
        medicines = medicines.filter(category=selected_category)

    return render(request, 'inventory/medicines.html', {
        'page_title': 'Medicines',
        'medicines': medicines,
        'categories': Category.objects.all(),
        'selected_category': selected_category,
        'can_manage': can_manage_inventory(request.user),
    })


@login_required
def medicine_add(request):
    denied = _deny_if_not_manager(request)
    if denied:
        return denied

    initial = {}
    category_id = request.GET.get('category')
    if category_id and category_id.isdigit() and Category.objects.filter(pk=category_id).exists():
        initial['category'] = category_id

    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                medicine = _save_medicine(form)
            messages.success(request, f'{medicine.brand_name} was added successfully.')
            return redirect('medicines')
    else:
        form = MedicineForm(initial=initial)

    return render(request, 'inventory/medicine_form.html', {
        'page_title': 'Add Medicine',
        'form': form,
    })


@login_required
def medicine_edit(request, pk):
    denied = _deny_if_not_manager(request)
    if denied:
        return denied

    medicine = get_object_or_404(Medicine, pk=pk)

    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            with transaction.atomic():
                medicine = _save_medicine(form)
            messages.success(request, f'{medicine.brand_name} was updated successfully.')
            return redirect('medicines')
    else:
        form = MedicineForm(instance=medicine)

    return render(request, 'inventory/medicine_form.html', {
        'page_title': 'Edit Medicine',
        'form': form,
        'medicine': medicine,
    })


@login_required
def medicine_delete(request, pk):
    denied = _deny_if_not_manager(request)
    if denied:
        return denied

    medicine = get_object_or_404(Medicine, pk=pk)

    if request.method == 'POST':
        name = medicine.brand_name
        medicine.delete()
        messages.success(request, f'{name} was deleted.')
        return redirect('medicines')

    return render(request, 'inventory/medicine_confirm_delete.html', {
        'page_title': 'Delete Medicine',
        'medicine': medicine,
    })


@login_required
def barcode_lookup(request):
    """Return medicine details for a scanned barcode. Used by the POS later."""
    barcode = request.GET.get('barcode', '').strip()
    if not barcode:
        return JsonResponse({'found': False, 'error': 'Barcode is required.'}, status=400)

    try:
        record = MedicineBarcode.objects.select_related(
            'medicine__category', 'medicine__supplier'
        ).get(barcode=barcode)
    except MedicineBarcode.DoesNotExist:
        return JsonResponse({'found': False}, status=404)

    medicine = record.medicine
    return JsonResponse({
        'found': True,
        'barcode': record.barcode,
        'medicine': {
            'id': medicine.id,
            'brand_name': medicine.brand_name,
            'generic_name': medicine.generic_name,
            'category': medicine.category.name if medicine.category else '',
            'supplier': medicine.supplier.name if medicine.supplier else '',
            'dosage_form': medicine.dosage_form,
            'strength': medicine.strength,
            'unit': medicine.unit,
            'purchase_price': str(medicine.purchase_price),
            'selling_price': str(medicine.selling_price),
            'reorder_level': medicine.reorder_level,
            'description': medicine.description,
        },
    })


@login_required
def categories(request):
    categories = (
        Category.objects
        .annotate(medicine_count=Count('medicines'))
        .prefetch_related('medicines')
    )
    return render(request, 'inventory/categories.html', {
        'page_title': 'Categories',
        'categories': categories,
        'can_manage': can_manage_inventory(request.user),
    })


@login_required
def category_add(request):
    denied = _deny_if_not_manager(request, 'categories')
    if denied:
        return denied

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'{category.name} was added successfully.')
            return redirect('categories')
    else:
        form = CategoryForm()

    return render(request, 'inventory/category_form.html', {
        'page_title': 'Add Category',
        'form': form,
    })


@login_required
def category_edit(request, pk):
    denied = _deny_if_not_manager(request, 'categories')
    if denied:
        return denied

    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'{category.name} was updated successfully.')
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'inventory/category_form.html', {
        'page_title': 'Edit Category',
        'form': form,
        'category': category,
    })


@login_required
def category_delete(request, pk):
    denied = _deny_if_not_manager(request, 'categories')
    if denied:
        return denied

    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f'{name} was deleted.')
        return redirect('categories')

    return render(request, 'inventory/category_confirm_delete.html', {
        'page_title': 'Delete Category',
        'category': category,
    })


@login_required
def suppliers(request):
    suppliers = Supplier.objects.annotate(medicine_count=Count('medicines'))
    return render(request, 'inventory/suppliers.html', {
        'page_title': 'Suppliers',
        'suppliers': suppliers,
        'can_manage': can_manage_inventory(request.user),
    })


@login_required
def supplier_add(request):
    denied = _deny_if_not_manager(request, 'suppliers')
    if denied:
        return denied

    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f'{supplier.name} was added successfully.')
            return redirect('suppliers')
    else:
        form = SupplierForm()

    return render(request, 'inventory/supplier_form.html', {
        'page_title': 'Add Supplier',
        'form': form,
    })


@login_required
def supplier_edit(request, pk):
    denied = _deny_if_not_manager(request, 'suppliers')
    if denied:
        return denied

    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f'{supplier.name} was updated successfully.')
            return redirect('suppliers')
    else:
        form = SupplierForm(instance=supplier)

    return render(request, 'inventory/supplier_form.html', {
        'page_title': 'Edit Supplier',
        'form': form,
        'supplier': supplier,
    })


@login_required
def supplier_delete(request, pk):
    denied = _deny_if_not_manager(request, 'suppliers')
    if denied:
        return denied

    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == 'POST':
        name = supplier.name
        supplier.delete()
        messages.success(request, f'{name} was deleted.')
        return redirect('suppliers')

    return render(request, 'inventory/supplier_confirm_delete.html', {
        'page_title': 'Delete Supplier',
        'supplier': supplier,
    })


@login_required
def stocks(request):
    return _placeholder(request, 'stocks')


@login_required
def expiry_dates(request):
    return _placeholder(request, 'expiry_dates')


@login_required
def alerts(request):
    return _placeholder(request, 'alerts')
