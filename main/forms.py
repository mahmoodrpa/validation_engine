from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()

class TransformDataForm(forms.Form):
    group_promo_validation = forms.BooleanField(required=False)
    group_amazon_promo = forms.BooleanField(required=False)
    po_calculation = forms.BooleanField(required=False)
    validation_rules= forms.BooleanField(required=False)
    promo_calculation= forms.BooleanField(required=False)
    
# class DeleteDataForm(forms.Form):
#     delete_remit = forms.BooleanField(required=False)
#     delete_promoagreement = forms.BooleanField(required=False)
#     delete_promobackup = forms.BooleanField(required=False)
#     delete_promo_group = forms.BooleanField(required=False)
#     delete_podata = forms.BooleanField(required=False)
#     delete_grouppodata = forms.BooleanField(required=False)
#     delete_promo_validation = forms.BooleanField(required=False)
#     delete_rules = forms.BooleanField(required=False)
#     delete_costco_un_backup = forms.BooleanField(required=False)
#     delete_price_increase = forms.BooleanField(required=False)
#     delete_discontinued_items = forms.BooleanField(required=False)
#     delete_product_master = forms.BooleanField(required=False)
#     delete_swell_terms = forms.BooleanField(required=False)
#     delete_vbrp = forms.BooleanField(required=False)
#     unsalable_combined = forms.BooleanField(required=False)
#     unsalable_rules = forms.BooleanField(required=False)


class DeleteDataForm(forms.Form):
    delete_hrc = forms.BooleanField(required=False) 
    delete_vbrk = forms.BooleanField(required=False)
    delete_vbrp = forms.BooleanField(required=False)
    delete_zoa = forms.BooleanField(required=False)   
    delete_deduction =forms.BooleanField(required=False)           


class AddUserForm(UserCreationForm):
    is_staff = forms.BooleanField(label='Staff Status', required=False)
    is_superuser = forms.BooleanField(label='Superuser Status', required=False)
    is_active = forms.BooleanField(label='Active Status', required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active']
        # fields = ['username',  'is_staff', 'is_superuser', 'is_active']

class ModifyUserPermissionsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_active', 'is_staff', 'is_superuser',]        



class CustomPasswordChangeForm(PasswordChangeForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError('This email address is already in use. Please provide a different one.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        email = cleaned_data.get('email')

        if not first_name:
            self.add_error('first_name', 'First name is required.')

        if not email:
            self.add_error('email', 'Email is required.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name', user.first_name)
        user.last_name = self.cleaned_data.get('last_name', user.last_name)
        user.email = self.cleaned_data.get('email', user.email)
        if commit:
            user.save()
        return user