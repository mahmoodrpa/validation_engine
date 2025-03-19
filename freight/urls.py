from django.contrib import admin
from django.urls import path, include
from freight import views as fv

urlpatterns = [
    path('freight_deductions/', fv.deductions_view, name='freight_deductions_view'),
    path('freight_backup/', fv.backup_view, name='freight_backup_view'),   
    path('transform_freight_data/', fv.transform_freight_data, name='transform_freight_data'),   
    path('delete_freight_data/', fv.delete_freight_data, name='delete_freight_data'),   
    path('freight_validation_view/', fv.freight_validation_view, name='freight_validation_view'), 
    
]
