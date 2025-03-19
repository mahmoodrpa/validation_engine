from django import forms
# from .models import PDFFile,POD_details
from .models import pod_detail
from django.core.exceptions import ValidationError
import os

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()

class TransformDataForm(forms.Form):    
    osd_validation=forms.BooleanField(required=False)    
    osd_calculations=forms.BooleanField(required=False)
    deductions_calculations=forms.BooleanField(required=False)
    
  

class DeleteDataForm(forms.Form):
    delete_deduction = forms.BooleanField(required=False, label='Delete Deduction Data')
    delete_backup = forms.BooleanField(required=False, label='Delete Backup Data')
    delete_invoice_data = forms.BooleanField(required=False, label='Delete Invoice Data')
    delete_validation = forms.BooleanField(required=False, label='Delete Validation Data')

def validate_pdf_files(value):
    ext = os.path.splitext(value.name)[1]
    if ext.lower() !=".pdf":
        raise ValidationError("Only PDF Files are allowed")


class PODUploadForm(forms.ModelForm):
    class Meta:
        model = pod_detail
        fields = ['pod_file']  

    def clean(self):
        cleaned_data = super().clean()
        pod_file = cleaned_data.get('pod_file')

        if pod_file:
            # Set the 'title' field to the name of the uploaded file
            cleaned_data['Title'] = pod_file.name

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Set the 'pdf_file' field to the uploaded file directly
        instance.pod_file = self.cleaned_data['pod_file']

        if commit:
            instance.save()

        return instance



class PODDetailsForm(forms.ModelForm):
    class Meta:
        model = pod_detail
        fields = [           
            'pod_file',
            'order_number',
            'invoice_number',
            'bol',
            'sku',
            'shortage',
            'damage',
            'returns',
            'overage',
            'net_shortage',
            'customer_sign',
            'carrier_sign',
            'subject_to_count',
            'pod_found'
        ]

        widgets = {
            # 'inv_sku': forms.TextInput(attrs={'class': 'form-control'}),
            'pod_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'order_number': forms.TextInput(attrs={'class': 'form-control'}),
            'invoice_number': forms.TextInput(attrs={'class': 'form-control'}),
            'bol': forms.TextInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'shortage': forms.NumberInput(attrs={'class': 'form-control'}),
            'damage': forms.NumberInput(attrs={'class': 'form-control'}),
            'returns': forms.NumberInput(attrs={'class': 'form-control'}),
            'overage': forms.NumberInput(attrs={'class': 'form-control'}),
            'net_shortage': forms.NumberInput(attrs={'class': 'form-control'}),
            'customer_sign': forms.TextInput(attrs={'class': 'form-control'}),
            'carrier_sign': forms.TextInput(attrs={'class': 'form-control'}),
            'subject_to_count': forms.TextInput(attrs={'class': 'form-control'}),
            'pod_found': forms.TextInput(attrs={'class': 'form-control'}),
        }