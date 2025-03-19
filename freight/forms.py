from django import forms
from django.core.exceptions import ValidationError
import os

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()

class TransformDataForm(forms.Form):    
    freight_validation=forms.BooleanField(required=False)    
    freight_calculations=forms.BooleanField(required=False)
    
  

class DeleteDataForm(forms.Form):
    delete_deduction = forms.BooleanField(required=False, label='Delete Deduction Data')
    delete_backup = forms.BooleanField(required=False, label='Delete Backup Data')
    delete_invoice_data = forms.BooleanField(required=False, label='Delete Invoice Data')
    delete_validation = forms.BooleanField(required=False, label='Delete Validation Data')

