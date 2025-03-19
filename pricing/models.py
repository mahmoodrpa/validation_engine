from django.db import models


class deduction_data(models.Model):
    ids = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    deduction_date = models.DateField(blank=True, null=True, db_index=False)
    customer_name = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    customer_account = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    standard_customer = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    deduction_reference = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    invoice_number = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    deduction_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_index=False)
    deduction_reason = models.TextField(blank=True, null=True, db_index=False)
    payment_number = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    backup_status = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    invoice_status = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    validation = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    invalid_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_index=False)
    valid_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_index=False)
    billback = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    billback_date = models.DateField(blank=True, null=True, db_index=False)
    billback_amount = models.DecimalField(max_digits=10, decimal_places=2, db_index=False)
    recovery_status = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    recovered_amount = models.DecimalField(max_digits=10, decimal_places=2, db_index=False)


class backup_data(models.Model):
    ids = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    inv_sku = models.CharField(max_length=100, null=True,blank=True) #calculated field
    standard_customer = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    invoice_number = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    sku = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    deducted_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_index=False)
    deducted_qty = models.IntegerField(blank=True, null=True, db_index=False)
    deducted_price_per_qty = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_index=False)
    deduction_date = models.DateField(blank=True, null=True, db_index=False)
    invoice_location = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    reason_code = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    sub_reason_code = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    deduction_reason = models.TextField(blank=True, null=True, db_index=False)
    backup_status = models.CharField(max_length=255, blank=True, null=True, db_index=False)

class price_change(models.Model):
    sku = models.CharField(max_length=50, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pack_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    case_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    units_per_case = models.IntegerField(null=True, blank=True)
    units_per_pack = models.IntegerField(null=True, blank=True)
    packs_per_case = models.IntegerField(null=True, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    communication_date = models.DateField(null=True, blank=True)
    BUYER_APPROVAL_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )
    buyer_approved = models.CharField(max_length=3, choices=BUYER_APPROVAL_CHOICES, default='no',null=True, blank=True)


class pricing_validation(models.Model):
    #fields from backup_data
    inv_sku = models.CharField(max_length=100, null=True,blank=True) #calculated field
    ids = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    invoice_number = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    sku = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    deducted_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_index=False)
    deducted_qty = models.IntegerField(blank=True, null=True, db_index=False)
    deducted_price_per_qty = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_index=False)
    deduction_reason = models.TextField(blank=True, null=True, db_index=False)
    

    # fields from deduction data
    ids = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    deduction_date = models.DateField(null=True, blank=True)
    standard_customer = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    deduction_reference = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    payment_number = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    

    #fields from invoice data
    invoice_date = models.DateField(null=True, blank=True)
    billed_qty = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    gross_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    net_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gross_price_per_qty = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    net_price_per_qty = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    customer_expected_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    #fields from price change
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pack_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    case_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    units_per_case = models.IntegerField(null=True, blank=True)
    units_per_pack = models.IntegerField(null=True, blank=True)
    packs_per_case = models.IntegerField(null=True, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    communication_date = models.DateField(null=True, blank=True)
    BUYER_APPROVAL_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )   
    buyer_approved = models.CharField(max_length=3, choices=BUYER_APPROVAL_CHOICES, default='no', null=True, blank=True)

    #calculated fields    
    # customer_expected_price_lower_than_billed = models.BooleanField(null=True, blank=True)
    customer_expected_price_lower_than_billed = models.CharField(max_length=50, null=True, blank=True)
    price_change_not_communicated = models.CharField(max_length=50, null=True, blank=True)
    price_change_communicated_late = models.CharField(max_length=50, null=True, blank=True)
    unit_of_measurement_issue = models.CharField(max_length=50, null=True, blank=True)
    # qty_ded_vs_Billed_issue = models.BooleanField(null=True, blank=True)
    qty_ded_vs_Billed_issue = models.CharField(max_length=50, null=True, blank=True)
    mod_issue = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    validation_status = models.CharField(max_length=50, null=True, blank=True)
    invalid_amount = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank = True)
    valid_amount = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank = True)
    detailed_reason = models.CharField(max_length=50, null=True, blank=True)