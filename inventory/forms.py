import re

from django import forms

from .models import Category, Medicine, MedicineBarcode, Supplier


class MedicineForm(forms.ModelForm):
    new_category = forms.CharField(
        label='Add New Category',
        required=False,
    )
    new_supplier = forms.CharField(
        label='Add New Supplier',
        required=False,
    )
    barcodes = forms.CharField(
        label='Register Medicine Barcode',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
    )

    class Meta:
        model = Medicine
        fields = [
            'brand_name',
            'generic_name',
            'category',
            'supplier',
            'dosage_form',
            'strength',
            'unit',
            'purchase_price',
            'selling_price',
            'reorder_level',
            'description',
        ]
        labels = {
            'brand_name': 'Brand Name',
            'generic_name': 'Generic Name',
            'category': 'Category',
            'supplier': 'Supplier',
            'dosage_form': 'Dosage Form',
            'strength': 'Strength',
            'unit': 'Unit',
            'purchase_price': 'Purchase Price',
            'selling_price': 'Selling Price',
            'reorder_level': 'Reorder Level',
            'description': 'Description (optional)',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.fields['supplier'].required = False

        if self.instance and self.instance.pk:
            self.fields['barcodes'].initial = '\n'.join(
                self.instance.barcodes.values_list('barcode', flat=True)
            )

    def clean_barcodes(self):
        raw = self.cleaned_data.get('barcodes', '')
        codes = [code.strip() for code in re.split(r'[\r\n]+', raw) if code.strip()]

        if len(codes) != len(set(codes)):
            raise forms.ValidationError('Duplicate barcodes are not allowed in one submission.')

        existing = MedicineBarcode.objects.filter(barcode__in=codes)
        if self.instance and self.instance.pk:
            existing = existing.exclude(medicine=self.instance)

        duplicates = list(existing.values_list('barcode', flat=True))
        if duplicates:
            raise forms.ValidationError('Already registered: ' + ', '.join(duplicates))

        return codes


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'contact_number', 'email', 'address', 'lead_time_days', 'status']
        labels = {
            'name': 'Supplier Name',
            'contact_person': 'Contact Person',
            'contact_number': 'Contact Number',
            'email': 'Email',
            'address': 'Address',
            'lead_time_days': 'Lead Time Days',
            'status': 'Status',
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        labels = {
            'name': 'Category Name',
            'description': 'Description',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

