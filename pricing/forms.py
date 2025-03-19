from django import forms
from django.core.exceptions import ValidationError
import os

class TransformDataForm(forms.Form):
    group_pricing = forms.BooleanField(required=False)
    backup_data_calculation = forms.BooleanField(required=False)
    validation_data_calculation = forms.BooleanField(required=False)
    
class DeleteDataForm(forms.Form):
    delete_deductions = forms.BooleanField(required=False)
    delete_invoice_data = forms.BooleanField(required=False)
    delete_backup = forms.BooleanField(required=False)
    delete_price_change = forms.BooleanField(required=False)
    delete_pricing_validation = forms.BooleanField(required=False)


