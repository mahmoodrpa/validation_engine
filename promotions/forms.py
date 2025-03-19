from django import forms

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()

class TransformDataForm(forms.Form):
    group_promo_validation = forms.BooleanField(required=False)
    group_amazon_promo = forms.BooleanField(required=False)
    po_calculation = forms.BooleanField(required=False)
    validation_rules= forms.BooleanField(required=False)
    promo_calculation= forms.BooleanField(required=False)
    
class DeleteDataForm(forms.Form):
    delete_remit = forms.BooleanField(required=False)
    delete_promoagreement = forms.BooleanField(required=False)
    delete_promobackup = forms.BooleanField(required=False)
    delete_promo_group = forms.BooleanField(required=False)
    delete_podata = forms.BooleanField(required=False)
    delete_grouppodata = forms.BooleanField(required=False)
    delete_promo_validation = forms.BooleanField(required=False)
    delete_rules = forms.BooleanField(required=False)
    delete_costco_un_backup = forms.BooleanField(required=False)
    delete_price_increase = forms.BooleanField(required=False)
    delete_discontinued_items = forms.BooleanField(required=False)
    delete_product_master = forms.BooleanField(required=False)
    delete_swell_terms = forms.BooleanField(required=False)
    delete_vbrp = forms.BooleanField(required=False)
    unsalable_combined = forms.BooleanField(required=False)
    unsalable_rules = forms.BooleanField(required=False)