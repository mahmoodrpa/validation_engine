from django.contrib import admin
from django.urls import path, include
from pricing import views as pc

urlpatterns = [
    path('pricing_deductions/', pc.deductions_view, name='pricing_deductions_view'),
    path('pricing_backup/', pc.backup_view, name='pricing_backup_view'),
    path('price_change_data/', pc.price_change_data, name='price_change_data'),
    path('transform_pricing_data/', pc.transform_pricing_data, name='transform_pricing_data'),
    path('transform_pricing_data/', pc.transform_pricing_data, name='transform_pricing_data'),
    path('pricing_validation_engine/', pc.pricing_validation_view, name='pricing_validation_engine'),
    path('delete_pricing_data/', pc.delete_data, name='delete_pricing_data'),
    ]
