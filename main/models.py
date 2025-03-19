from django.db import models
from django.contrib.auth.models import User
from django.db import connection
import os

# Create your models here.
class user_data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_login = models.BooleanField(default=True)

class Category(models.Model):
    category = models.CharField(max_length=50)
    retailer = models.CharField(max_length=50, null=True, blank=True)
    subcategories = models.CharField(max_length=50, null=True, blank=True)

    
class UploadRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filetype = models.CharField(max_length=255)
    filepath = models.CharField(max_length=255)
    num_rows = models.IntegerField(default=0)
    progress = models.IntegerField(default=0)
    status = models.CharField(max_length=255, default='Upload requested')
    model_name = models.CharField(max_length=255)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.filepath

# def custom_upload_path(instance, filename):
#     return filename

def custom_upload_path(instance, filename):      
    subfolder = 'Uploads'   
    full_path =  subfolder   
    if not os.path.exists(full_path):
        os.makedirs(full_path)    
    return os.path.join(full_path, filename)

class UploadedCSV(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=custom_upload_path, default='NoFile.csv')
    num_rows = models.PositiveIntegerField()
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    total_time = models.DurationField(null=True, blank=True)
    STATUS_CHOICES = (
        ('started', 'Started'),
        ('inprogress', 'In Progress'),
        ('completed', 'Completed'),
    )
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='started')



class test(models.Model):
    name = models.CharField(max_length=255)
    phone =models.CharField(max_length=255)

class test_ref(models.Model):
    account =models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone =models.CharField(max_length=255)

class invoice_data(models.Model):
    inv_sku = models.CharField(max_length=255, blank=True, null=True)
    invoice_number = models.CharField(max_length=255, blank=True, null=True)
    invoice_date = models.DateField(null=True, blank=True)
    sku = models.CharField(max_length=255, blank=True, null=True)
    billed_qty = models.IntegerField(blank=True, null=True)
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