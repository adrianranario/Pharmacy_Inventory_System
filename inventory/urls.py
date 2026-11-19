from django.urls import path

from . import views

urlpatterns = [
    path('', views.medicines, name='inventory-home'),
    path('medicines/', views.medicines, name='medicines'),
    path('medicines/add/', views.medicine_add, name='medicine-add'),
    path('medicines/<int:pk>/edit/', views.medicine_edit, name='medicine-edit'),
    path('medicines/<int:pk>/delete/', views.medicine_delete, name='medicine-delete'),
    path('barcode-lookup/', views.barcode_lookup, name='barcode-lookup'),
    path('categories/', views.categories, name='categories'),
    path('categories/add/', views.category_add, name='category-add'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category-edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category-delete'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('suppliers/add/', views.supplier_add, name='supplier-add'),
    path('suppliers/<int:pk>/edit/', views.supplier_edit, name='supplier-edit'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete, name='supplier-delete'),
    path('stocks/', views.stocks, name='stocks'),
    path('expiry-dates/', views.expiry_dates, name='expiry-dates'),
    path('alerts/', views.alerts, name='alerts'),
]
