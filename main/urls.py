from django.contrib import admin
from django.urls import path, include
from main import views

urlpatterns = [
    path('invoice_data_view/', views.invoice_view, name='invoice_view'),
    path('reporting/', views.reporting, name='reporting'),
    # path('create_billback_package/', views.create_billback_package, name='create_billback_package'),
   
]