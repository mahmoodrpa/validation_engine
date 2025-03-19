from django.db import models
from django.contrib.auth.models import User
from django.db import connection

# Create your models here.

class amazonremittance(models.Model):
    payment_number = models.CharField(max_length=50, null=True, blank=True)
    invoice_number = models.CharField(max_length=50, null=True, blank=True)
    invoice_date= models.DateField(null=True, blank=True)
    description = models.CharField(max_length=50, null=True, blank=True)
    invoice_amount = models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    invoice_currency = models.CharField(max_length=50, null=True, blank=True)
    withholding_amount = models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    terms_discount = models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    deduction_amount = models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    remaining_amount = models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    payment_amount = models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    deduction_reason = models.CharField(max_length=50, null=True, blank=True)
    sub_reason = models.CharField(max_length=50, null=True, blank=True)

class amazonpromo(models.Model):
    
    Deduction_ref =models.CharField(max_length=50, null=True, blank=True) 
    Unique_promo = models.CharField(max_length=50, null=True, blank=True)
    Receive_Date=models.DateField(null=True, blank=True)
    Return_Date=models.DateField(null=True, blank=True)
    Invoice_Day=models.DateField(null=True, blank=True)
    Transaction_Type=models.CharField(max_length=50, null=True, blank = True)
    Quantity=models.DecimalField(decimal_places=0,max_digits=50, null=True, blank=True)
    Net_Receipts=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    Net_Receipts_Currency=models.CharField(max_length=50, null=True, blank = True)
    List_Price=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    List_Price_Currency=models.CharField(max_length=50, null=True, blank = True)
    Rebate_In_Agreement_Currency=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    Agreement_Currency=models.CharField(max_length=50, null=True, blank = True)
    Rebate_In_Purchase_Order_Currency=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    Purchase_Order_Currency=models.CharField(max_length=50, null=True, blank = True)
    Purchase_Order=models.CharField(max_length=50, null=True, blank = True)
    Promo_Asin=models.CharField(max_length=50, null=True, blank = True)
    UPC=models.CharField(max_length=50, null=True, blank = True)
    EAN=models.CharField(max_length=50, null=True, blank = True)
    Manufacturer=models.CharField(max_length=50, null=True, blank = True)
    Distributor=models.CharField(max_length=50, null=True, blank = True)
    Product_Group=models.CharField(max_length=50, null=True, blank = True)
    Category=models.CharField(max_length=50, null=True, blank = True)
    Subcategory=models.CharField(max_length=50, null=True, blank = True)
    Title=models.TextField(max_length=500, null=True, blank = True)
    Product_Description=models.TextField(max_length=500, null=True, blank = True)
    Binding=models.CharField(max_length=50, null=True, blank = True)
    Cost_Currency=models.CharField(max_length=50, null=True, blank = True)
    Old_Cost=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    New_Cost=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    Price_Protection_Agreement=models.CharField(max_length=50, null=True, blank = True)
    Price_Protection_Day=models.DateField(null=True, blank=True)
    Cost_Variance=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    Invoice=models.CharField(max_length=50, null=True, blank = True)

    def promo_calculation(self):
        update_unique_promo_sql = """
            UPDATE deduction_amazonpromo
            SET Unique_promo = Purchase_Order || Promo_Asin
            WHERE Unique_promo IS NULL OR Unique_promo = '';
        """

        # if self.Unique_promo is None or self.Unique_promo =="":
        #     self.Unique_promo = self.Purchase_Order + self.Promo_Asin
        # else:
        #     self.Unique_promo = self.Unique_promo
        with connection.cursor() as cursor:
            cursor.execute(update_unique_promo_sql)

        self.save()

class amazonagreement(models.Model):
    INVOICE_NUMBER = models.CharField(max_length=50, null=True, blank=True)
    INVOICE_DATE=models.DateField(null=True, blank=True)
    PAYMENT_TERM=models.CharField(max_length=50, null=True, blank=True)
    DUE_DATE=models.DateField(null=True, blank=True)
    BUYER=models.CharField(max_length=50, null=True, blank=True)
    PUB_CODE=models.CharField(max_length=50, null=True, blank=True)
    AGREEMENT_num=models.CharField(max_length=50, null=True, blank=True)
    PAYMENT_METHOD=models.CharField(max_length=50, null=True, blank=True)
    TRANSACTION_TYPE=models.CharField(max_length=50, null=True, blank=True)
    PRODUCT_LINE=models.CharField(max_length=50, null=True, blank=True)
    PO_NUMBER=models.CharField(max_length=50, null=True, blank=True)
    LINE_NUMBER=models.CharField(max_length=50, null=True, blank=True)
    QUANTITY_ORDERED=models.CharField(max_length=50, null=True, blank = True)
    QUANTITY_CREDITED=models.CharField(max_length=50, null=True, blank = True)
    QUANTITY_INVOICED=models.CharField(max_length=50, null=True, blank = True)
    UNIT_STANDARD_PRICE=models.CharField(max_length=50, null=True, blank = True)
    UNIT_SELLING_PRICE=models.CharField(max_length=50, null=True, blank = True)
    REVENUE_AMOUNT=models.CharField(max_length=50, null=True, blank = True)
    SALES_ORDER=models.CharField(max_length=50, null=True, blank=True)
    SALES_ORDER_LINE=models.CharField(max_length=50, null=True, blank=True)
    DESCRIPTION=models.CharField(max_length=50, null=True, blank=True)
    REBATE_prct=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    AGREEMENT_END=models.DateField(null=True, blank=True)

class amazonpodata(models.Model):
    Unique_key=models.CharField(max_length=50, null=True, blank = True)
    Trim_PO=models.CharField(max_length=50, null=True, blank = True)
    Trim_ASIN=models.CharField(max_length=50, null=True, blank = True)
    PO=models.CharField(max_length=50, null=True, blank = True)
    PO_ASIN=models.CharField(max_length=50, null=True, blank = True)
    External_ID=models.CharField(max_length=50, null=True, blank = True)
    External_Id_Type=models.CharField(max_length=50, null=True, blank = True)
    Model_Number=models.CharField(max_length=50, null=True, blank = True)
    Title=models.TextField(max_length=500, null=True, blank = True)
    Availability=models.CharField(max_length=50, null=True, blank = True)
    Backordered=models.CharField(max_length=50, null=True, blank = True)
    Window_Type=models.CharField(max_length=50, null=True, blank = True)
    Window_Start=models.DateField(null=True, blank=True)
    Window_End=models.DateField(null=True, blank=True)
    Expected_Date=models.DateField(null=True, blank=True)
    Case_Size=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    Quantity_Requested=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    Accepted_Quantity=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    Quantity_received=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    Quantity_Outstanding=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    Case_Cost=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    Total_Cost=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    Eaches_Quantity=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)

class PromoGroup(models.Model):

    Deduction_ref = models.CharField(max_length=50, null=True, blank = True)
    unique_promo =models.CharField(max_length=50, null=True, blank = True)
    Receive_Date=models.DateField(null=True, blank=True)
    Return_Date=models.DateField(null=True, blank=True)
    Invoice_Day=models.DateField(null=True, blank=True)
    Transaction_Type=models.CharField(max_length=50, null=True, blank = True)
    Quantity=models.DecimalField(decimal_places=0,max_digits=50, null=True, blank=True)
    Net_Receipts=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    Net_Receipts_Currency=models.CharField(max_length=50, null=True, blank = True)
    List_Price=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    List_Price_Currency=models.CharField(max_length=50, null=True, blank = True)
    Rebate_In_Agreement_Currency=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    Agreement_Currency=models.CharField(max_length=50, null=True, blank = True)
    Rebate_In_Purchase_Order_Currency=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    Purchase_Order_Currency=models.CharField(max_length=50, null=True, blank = True)
    Purchase_Order=models.CharField(max_length=50, null=True, blank = True)
    Promo_Asin=models.CharField(max_length=50, null=True, blank = True)
    UPC=models.CharField(max_length=50, null=True, blank = True)
    EAN=models.CharField(max_length=50, null=True, blank = True)
    Manufacturer=models.CharField(max_length=50, null=True, blank = True)
    Distributor=models.CharField(max_length=50, null=True, blank = True)
    Product_Group=models.CharField(max_length=50, null=True, blank = True)
    Category=models.CharField(max_length=50, null=True, blank = True)
    Subcategory=models.CharField(max_length=50, null=True, blank = True)
    Title=models.TextField(max_length=500, null=True, blank = True)
    Product_Description=models.TextField(max_length=500, null=True, blank = True)
    Binding=models.CharField(max_length=50, null=True, blank = True)
    Cost_Currency=models.CharField(max_length=50, null=True, blank = True)
    Old_Cost=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    New_Cost=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    Price_Protection_Agreement=models.CharField(max_length=50, null=True, blank = True)
    Price_Protection_Day=models.DateField(null=True, blank=True)
    Cost_Variance=models.DecimalField(decimal_places=2,max_digits=50, null=True, blank=True)
    Invoice=models.CharField(max_length=50, null=True, blank = True)

    def __str__(self):
        return str(self.unique_promo)

class PromoValidation(models.Model):
    # Fields from amazonremit
    payment_date = models.DateField(null=True, blank=True)
    invoice_number = models.CharField(max_length=50, null=True, blank=True)
    deduction_amount = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank=True)
    deduction_reason = models.CharField(max_length=50, null=True, blank=True)
    
    # Fields from promogroup
    unique_promo = models.CharField(max_length=50, null=True, blank=True)
    promo_quantity = models.DecimalField(decimal_places=0, max_digits=50, null=True, blank=True)
    net_receipts = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank=True)
    list_price = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank=True)
    purchase_order = models.CharField(max_length=50, null=True, blank=True)
    promo_asin = models.CharField(max_length=50, null=True, blank=True)
    rebate_in_agreement_currency = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank=True)
    
    # Fields from amazonpodata
    unique_key = models.CharField(max_length=50, null=True, blank=True)
    podata_po = models.CharField(max_length=50, null=True, blank=True)
    podata_asin = models.CharField(max_length=50, null=True, blank=True)
    case_size = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank=True)
    quantity_received = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank=True)
    case_cost = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank=True)
    total_cost = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank=True)
    eaches_quantity = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank=True)

    #Add fields from amazonagreement
    agreement_num=models.CharField(max_length=50, null=True, blank=True)
    rebate_percent=models.DecimalField(decimal_places=2, max_digits=50, null=True, blank=True)
    agreement_end=models.DateField(null=True, blank=True)
    


    # Add calculated fields
    unit_price = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank = True)
    quantity_variance = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank = True)
    actual_netreceipts = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank = True)
    netreceipts_variance = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank = True)
    
    
    
    valid_rebate_rate = models.CharField(max_length=50, null=True, blank=True)
    valid_po = models.CharField(max_length=50, null=True, blank=True)
    valid_sku = models.CharField(max_length=50, null=True, blank=True)
    price_variance = models.CharField(max_length=50, null=True, blank=True)
    qty_variance = models.CharField(max_length=50, null=True, blank=True)
    validation_status = models.CharField(max_length=50, null=True, blank=True)
    invalid_amount = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank = True)
    detailed_reason = models.CharField(max_length=50, null=True, blank=True)
    
    def validation_rules(self):
        # SQL query to update valid_rebate_rate
        update_unit_price = """
            UPDATE deduction_promovalidation
            SET unit_price = 
                CASE
                    WHEN net_receipts IS NOT NULL AND net_receipts <> 0 AND promo_quantity <> 0
                    THEN ROUND(net_receipts / promo_quantity, 2)
                    ELSE 0
                END
            WHERE unit_price IS NULL OR unit_price = '';
        """
        update_quantity_variance = """
            UPDATE deduction_promovalidation
            SET quantity_variance = 
                CASE
                    WHEN promo_quantity IS NOT NULL AND eaches_quantity IS NOT NULL AND promo_quantity <> 0
                    THEN promo_quantity - eaches_quantity
                    ELSE 0
                END
            WHERE quantity_variance IS NULL OR quantity_variance = '';
        """

        update_actual_netreceipts = """
            UPDATE deduction_promovalidation
            SET actual_netreceipts = 
                CASE
                    WHEN eaches_quantity IS NOT NULL
                    THEN eaches_quantity * unit_price
                    ELSE actual_netreceipts
                END
            WHERE actual_netreceipts IS NULL OR actual_netreceipts = '' OR actual_netreceipts = 0;
        """

        update_netreceipts_variance = """
            UPDATE deduction_promovalidation
            SET netreceipts_variance = 
                CASE
                    WHEN net_receipts IS NOT NULL AND actual_netreceipts IS NOT NULL AND net_receipts <> 0
                    THEN net_receipts - actual_netreceipts
                    ELSE netreceipts_variance
                END
            WHERE netreceipts_variance IS NULL OR netreceipts_variance = '' OR netreceipts_variance = 0;
        """


        update_valid_rebate_rate = """
            UPDATE deduction_promovalidation
            SET valid_rebate_rate = CASE
                WHEN valid_rebate_rate IS NULL OR valid_rebate_rate = ''
                    THEN CASE
                        WHEN net_receipts IS NOT NULL AND rebate_in_agreement_currency IS NOT NULL AND net_receipts != 0
                            THEN
                                CASE
                                    WHEN ROUND(rebate_in_agreement_currency / net_receipts, 3) <= ROUND(rebate_percent, 3)
                                        THEN 'Valid'
                                    ELSE 'Invalid'
                                END
                            ELSE 'Invalid (Division by zero)'
                        END
                ELSE valid_rebate_rate
            END;
        """
        update_valid_po = """
            UPDATE deduction_promovalidation
            SET valid_po = 
                CASE
                    WHEN valid_po IS NULL OR valid_po = ''
                    THEN
                        CASE
                            WHEN purchase_order = podata_po
                            THEN 'Valid'
                            ELSE 'Invalid'
                        END
                    ELSE valid_po
                END;
        """
        update_valid_sku = """
            UPDATE deduction_promovalidation
            SET valid_sku = 
                CASE
                    WHEN valid_sku IS NULL OR valid_sku = ''
                    THEN
                        CASE
                            WHEN promo_asin = podata_asin
                            THEN 'Valid'
                            ELSE 'Invalid'
                        END
                    ELSE valid_sku
                END;
        """
        update_qty_variance = """
            UPDATE deduction_promovalidation
            SET qty_variance = 
                CASE
                    WHEN qty_variance IS NULL OR qty_variance = ''
                    THEN
                        CASE
                            WHEN quantity_variance IS NOT NULL AND quantity_variance > 0
                            THEN 'Invalid'
                            ELSE 'Valid'
                        END
                    ELSE qty_variance
                END;
        """
        update_validation_status = """
            UPDATE deduction_promovalidation
            SET validation_status = 
                CASE
                    WHEN validation_status IS NULL OR validation_status = ''
                    THEN
                        CASE
                            WHEN valid_rebate_rate = 'Invalid'
                            THEN 'Invalid'
                            WHEN qty_variance = 'Invalid'
                            THEN 'Invalid'
                            WHEN valid_po = 'Invalid'
                            THEN 'Invalid'
                            WHEN valid_sku = 'Invalid'
                            THEN 'Invalid'
                            ELSE 'Valid'
                        END
                    ELSE validation_status
                END;
        """
        update_detailed_reason = """
                UPDATE deduction_promovalidation
                SET detailed_reason =
                CASE
                    WHEN detailed_reason IS NULL OR detailed_reason = ''
                    THEN
                        CASE
                            WHEN valid_po = 'Invalid'
                            THEN 'PO deducted is not billed in the system'
                            WHEN valid_sku = 'Invalid'
                            THEN 'ASIN deducted is not billed on PO'
                            WHEN qty_variance = 'Invalid'
                            THEN 'Quantity deducted is higher than received quantity'
                            WHEN valid_rebate_rate = 'Invalid'
                            THEN 'Rebate percent taken is higher than rebate percent allowed in the contract'
                            ELSE ''
                        END
                    ELSE detailed_reason
                END;
        """
        update_invalid_amount = """
                UPDATE deduction_promovalidation
                SET invalid_amount = 
                CASE
                    WHEN invalid_amount IS NULL OR invalid_amount = ''
                    THEN
                        CASE
                            
                            WHEN valid_po = 'Invalid'
                            THEN rebate_in_agreement_currency
                            WHEN valid_sku = 'Invalid'
                            THEN rebate_in_agreement_currency
                            WHEN qty_variance = 'Invalid'
                            THEN netreceipts_variance * rebate_percent
                            WHEN valid_rebate_rate = 'Invalid'
                            THEN (rebate_percent - (rebate_in_agreement_currency/net_receipts)) * promo_quantity
                            ELSE 0
                        END
                    ELSE invalid_amount
                END;
        """

        with connection.cursor() as cursor:
            cursor.execute(update_unit_price)
            cursor.execute(update_quantity_variance)
            cursor.execute(update_actual_netreceipts)
            cursor.execute(update_netreceipts_variance)
            cursor.execute(update_valid_rebate_rate)
            cursor.execute(update_valid_po)
            cursor.execute(update_valid_sku)
            cursor.execute(update_qty_variance)
            cursor.execute(update_validation_status)
            cursor.execute(update_detailed_reason)
            cursor.execute(update_invalid_amount)


            # cursor.execute(update_valid_po_sql)
            # cursor.execute(update_valid_sku_sql)

    # ...
    # Continue with the rest of the validation logic

        self.save()