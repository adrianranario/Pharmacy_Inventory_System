from django.urls import path

from . import views

urlpatterns = [
    path('', views.medicines, name='inventory-home'),
    path('medicines/', views.medicines, name='medicines'),
    path('categories/', views.categories, name='categories'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('stocks/', views.stocks, name='stocks'),
    path('expiry-dates/', views.expiry_dates, name='expiry-dates'),
    path('alerts/', views.alerts, name='alerts'),
]
