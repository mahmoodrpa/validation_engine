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


class invoice_data(models.Model):
    inv_sku = models.CharField(max_length=255, blank=True, null=True)
    invoice_number = models.CharField(max_length=255, blank=True, null=True)
    sku = models.CharField(max_length=255, blank=True, null=True)
    billed_qty = models.CharField(max_length=50,null=True,blank=True)
    gross_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    oi_deal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    promo_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cash_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    freight_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    others = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    net_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gross_price_per_qty = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    net_price_per_qty = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fuel_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    lane = models.CharField(max_length=255, blank=True, null=True)
    freight_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gross_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  
    total_freight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)   
    order_number = models.CharField(max_length=255, blank=True, null=True)
    bol = models.CharField(max_length=255, blank=True, null=True)  
    carrier = models.CharField(max_length=255, blank=True, null=True) 


class edi_master(models.Model):
    deduction_reason = models.CharField(max_length=255, blank=True, null=True)
    freight_code_master = models.CharField(max_length=255, blank=True, null=True)
    

class edi_actual(models.Model):
    invoice_number = models.CharField(max_length=255, blank=True, null=True)
    deduction_reason = models.CharField(max_length=255, blank=True, null=True)
    freight_code_actual = models.CharField(max_length=255, blank=True, null=True)

class freight_communication(models.Model):
    customer_account = models.CharField(max_length=255, blank=True, null=True)
    standard_customer = models.CharField(max_length=255, blank=True, null=True)
    communicated_lane = models.CharField(max_length=255, blank=True, null=True)
    communicated_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    communicated_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


class validation(models.Model):
    #fields from deductions
    ids_dd = models.CharField(max_length=255, blank=True, null=True)
    standard_customer = models.CharField(max_length=255, blank=True, null=True)
    customer_account = models.CharField(max_length=255, blank=True, null=True, db_index=False)
    deduction_reference = models.CharField(max_length=255, blank=True, null=True)
    deduction_date = models.DateField(blank=True, null=True)

    # fields from backup
    ids_bd = models.CharField(max_length=255, blank=True, null=True)
    invoice_number = models.CharField(max_length=255, blank=True, null=True)
    deducted_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    deducted_qty = models.IntegerField(blank=True, null=True)
    deducted_price_per_qty = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    deduction_reason = models.TextField(blank=True, null=True)

    #fields from invoice
    billed_qty = models.CharField(max_length=50,null=True,blank=True)
    gross_price_per_qty = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    net_price_per_qty = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    freight_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fuel_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    lane = models.CharField(max_length=255, blank=True, null=True)
    freight_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_freight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gross_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  

    #fields from edi_master
    freight_code_master = models.CharField(max_length=255, blank=True, null=True)
    
    #fields from edi_actual
    freight_code_actual = models.CharField(max_length=255, blank=True, null=True)

    #fields from freight_communication
    communicated_lane = models.CharField(max_length=255, blank=True, null=True)
    communicated_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    communicated_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

     #calculated fields
    load_wise = models.CharField(max_length=20, null=True)
    invalid_amt_1 = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    invoice_count = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    duplicate = models.CharField(max_length=20, null=True)
    invalid_amt_2 = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    rate_wise = models.CharField(max_length=20, null=True)
    invalid_amt_3 = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    edi_mismatch = models.CharField(max_length=20, null=True)
    invalid_amt_4 = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    validation_status = models.CharField(max_length=20, null=True)
    invalid_amt = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    valid_amt = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    final_rca=models.CharField(max_length=50, null=True, blank=True)