## pylint:disable=no.member
from django.template.loader import render_to_string
from main.utils import *
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import pandas as pd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import loader
from dateutil import parser
from pathlib import Path
from django.core.paginator import Paginator
from django.shortcuts import render
from .forms import *
from .models import *
import pandas as pd
from datetime import datetime
from django.db.models import Count, OuterRef, Subquery
from django.db.models import Sum, F, Value
from django.db.models.functions import Concat
from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.views.decorators.http import condition
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from main import models as mm
import time
from openpyxl import Workbook
from main import views as mv
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import CustomPasswordChangeForm
from django.contrib.auth.models import User
from .forms import ModifyUserPermissionsForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from osd import views as cv
from freight import views as fv
from pricing import views as pv
from django.db.models import Sum
from osd import models as om
from promotions import views as prv
import zipfile
import io


date_formats = ['%m-%d-%Y', '%m/%d/%Y']
# Create your views here.
@login_required
def admin_panel(request):
    users = User.objects.all()

    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            is_staff = form.cleaned_data['is_staff']
            is_superuser = form.cleaned_data['is_superuser']
            is_active = form.cleaned_data['is_active']

            user = form.save(commit=False)
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.is_active = is_active
            user.save()

            return redirect('admin_panel')

    else:
        form = AddUserForm()

    return render(request, 'admin_panel.html', {'users': users, 'form': form})

def user_list(request):
    users = UserProfile.objects.all()
    return render(request, 'user_list.html', {'users': users})

def user_details(request, username):
        print("Username:", username)
        user = get_object_or_404(User, username=username)

        if request.method == 'POST':
            form = ModifyUserPermissionsForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('user_details', username=username)
        else:
            form = ModifyUserPermissionsForm(instance=user)

        return render(request, 'user_details.html', {'user': user, 'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')

class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    first_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    template_name = 'password_change.html'
    success_url = reverse_lazy('login')
    success_message = 'Your password and profile information were successfully updated.'
    
    
    def form_valid(self, form):
        print("Form is valid.")
        response = super().form_valid(form)

        # Add print statements to debug the form data
        print("First Name:", form.cleaned_data.get('first_name'))
        print("Last Name:", form.cleaned_data.get('last_name'))
        print("Email:", form.cleaned_data.get('email'))

        # Add print statements to check if save method is being called
        user = form.save()
        print("User information updated:", user)

        return response

    def form_invalid(self, form):
        print("Form is invalid.")
        print("Form Errors:", form.errors)
        return super().form_invalid(form)


def user_login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        passwrd = request.POST.get('password')
        user = authenticate(request, username=uname, password=passwrd)

        if user is not None:
            login(request, user)

            # Debugging prints
            print(f"user.is_active: {user.is_active}")
            print(f"user.first_name: {user.first_name}")
            print(f"user.email: {user.email}")

            # Check if the user is active
            # if not user.is_active:
                # Check if first_name or email is None
            if not user.first_name or not user.email :                
                # print("Redirecting to password_change")
                # return redirect('password_change')
                return redirect('index')

            # Redirect to the index page
            print("Redirecting to index")
            return redirect('index')
        else:
            messages.error(request, 'Username or Password is Incorrect !!')

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('user_login')

# @login_required(login_url="/login/")
# def index(request):
#     context = {
#         "entries": "Test"
#     }
#     return render(request, 'home.html', context)

# @login_required(login_url="/login/")
# def index(request):
#    labels1,values1 = top_customer_deduction_chart(request)
#    print(labels1,values1) 
#    context = {
#         'datapoints1': {
#             'labels': labels1,
#             'data': values1
#         }
#     }
#    return render(request, 'home.html',context)

def top_customer_deduction_chart(request):
    # Query to get the sum of deduction_amount for each standard_customer
    data = (om.deduction_data.objects
            .values('standard_customer')
            .annotate(total_amount=Sum('deduction_amount')/1000000)
            .order_by('-total_amount')[:10])  # Order by descending and limit to top 8
    
    # Prepare data for chart1 (Bar Chart)
    labels1 = [item['standard_customer'] for item in data]
    values1 = [float(item['total_amount']) for item in data]

    # Get the total deduction amount for the rest of the customers (others)
    top_customers_sum = [item['standard_customer'] for item in data]
    others_amount = (om.deduction_data.objects
                     .exclude(standard_customer__in=top_customers_sum)
                     .aggregate(total_amount=Sum('deduction_amount') / 1000000)['total_amount'] or 0)
    # Add 'Others' to the chart1 data if there's any amount for other customers
    if others_amount > 0:
        labels1.append('Others')
        values1.append(float(others_amount))
    
    return labels1,values1

def top_customer_count_chart(request):
    # Get top 8 customers by transaction count
    top_customers = (om.deduction_data.objects
                     .values('standard_customer')
                     .annotate(transaction_count=Count('id'))
                     .order_by('-transaction_count')[:10])
    
    # Get total transactions for the rest of the customers
    top_customers_ids = [customer['standard_customer'] for customer in top_customers]
    others_count = (om.deduction_data.objects
                    .exclude(standard_customer__in=top_customers_ids)
                    .aggregate(total_transactions=Count('id'))['total_transactions'] or 0)

    
    # Prepare data for chart2 (Bar Chart)
    labels2 = [customer['standard_customer'] for customer in top_customers]
    values2 = [customer['transaction_count'] for customer in top_customers]
    
    # Add 'Others' to the chart data
    if others_count > 0:
        labels2.append('Others')
        values2.append(others_count)
    
    return labels2,values2

def summary_deductions(request):
    # Calculate the unique customer count
    unique_customer_count = om.deduction_data.objects.values('standard_customer').distinct().count()

    # Get total deduction, count, and invalid amounts
    total_deduction = om.workflow.objects.aggregate(Sum('deducted_amount'))['deducted_amount__sum'] or 0
    deduction_count = om.workflow.objects.count()
    total_invalid = om.validation.objects.filter(validation_status='Invalid').aggregate(Sum('invalid_amount'))['invalid_amount__sum'] or 0
    invalid_count = om.validation.objects.filter(validation_status='Invalid').count()
    total_valid = om.validation.objects.filter(validation_status='Valid').aggregate(Sum('valid_amount'))['valid_amount__sum'] or 0
    valid_count = om.validation.objects.filter(validation_status='Valid').count()
    
    # Convert total amounts to millions
    total_deduction = total_deduction / 1000000
    total_invalid = total_invalid / 1000000
    total_valid = total_valid / 1000000

    # Calculate the unique customer count
    unique_customer_workflow = om.workflow.objects.values('standard_customer').distinct().count()
    
    # Get total deduction, count, and invalid amounts
    # total_deduction_validation = om.workflow.objects.aggregate(Sum('deducted_amount'))['deducted_amount__sum'] or 0
    
    deduction_count_validation = om.workflow.objects.values('invoice_number').count()
    pending_deduction_validation = om.workflow.objects.filter(validation_status='Pending Validation').aggregate(Sum('deducted_amount'))['deducted_amount__sum'] or 0
    pending_count_validation = om.workflow.objects.filter(validation_status='Pending Validation').count()
    total_invalid_validation = om.workflow.objects.filter(validation_status='Invalid').aggregate(Sum('invalid_amount'))['invalid_amount__sum'] or 0
    # invalid_count_validation = om.validation.objects.filter(validation_status='Invalid').count()
    invalid_count_validation =(
        om.workflow.objects
        .filter(validation_status='Invalid')  # Filter for 'Invalid' status
        .values('invoice_number')  # Get unique 'invoice_number'
        .distinct()  # Ensure distinct invoice numbers
        .count()  # Count the distinct records
    )
    total_valid_validation = om.workflow.objects.filter(validation_status='Valid').aggregate(Sum('valid_amount'))['valid_amount__sum'] or 0
    valid_count_validation = deduction_count_validation-invalid_count_validation - pending_count_validation
    total_deduction_validation = total_invalid_validation+total_valid_validation+pending_deduction_validation

    # pending validation split
    pending_missing_invoice = om.workflow.objects.filter(invalid_reason='Missing Invoice Data').aggregate(Sum('deducted_amount'))['deducted_amount__sum'] or 0
    missing_customer_sign = om.workflow.objects.filter(invalid_reason='Customer sign is missing on POD').aggregate(Sum('deducted_amount'))['deducted_amount__sum'] or 0
    missing_carrier_sign = om.workflow.objects.filter(invalid_reason='Carrier sign is missing on POD').aggregate(Sum('deducted_amount'))['deducted_amount__sum'] or 0
    pending_subject_to_count = om.workflow.objects.filter(invalid_reason='POD is subject to count').aggregate(Sum('deducted_amount'))['deducted_amount__sum'] or 0

    # Convert total amounts to millions
    total_deduction_validation = total_deduction_validation / 1000000
    total_invalid_validation = total_invalid_validation / 1000000
    total_valid_validation = total_valid_validation / 1000000
    pending_deduction_validation=pending_deduction_validation/1000000
    pending_missing_invoice=pending_missing_invoice/1000000
    missing_customer_sign=missing_customer_sign/1000000
    missing_carrier_sign=missing_carrier_sign/1000000
    pending_subject_to_count=pending_subject_to_count/1000000
    
    return total_deduction,deduction_count,total_invalid,invalid_count,total_valid,valid_count,unique_customer_count,unique_customer_workflow,total_deduction_validation,deduction_count_validation,total_invalid_validation,invalid_count_validation,total_valid_validation,valid_count_validation,pending_deduction_validation,pending_count_validation,pending_missing_invoice,missing_customer_sign,missing_carrier_sign,pending_subject_to_count

def priortized_customer_deduction(request):
    # Query to get the sum of deduction_amount for each standard_customer
    validation_data = (om.workflow.objects
            .values('standard_customer')
            .annotate(total_amount_validation=Sum('deducted_amount')/1000000)
            .order_by('-total_amount_validation')[:8])  # Order by descending and limit to top 8
    
    # Prepare data for chart3 (Bar Chart)
    labels3 = [item['standard_customer'] for item in validation_data]
    values3 = [float(item['total_amount_validation']) for item in validation_data]

    # Get the total deduction amount for the rest of the customers (others)
    priortized_customers_sum = [item['standard_customer'] for item in validation_data]
    others_amount_validation = (om.validation.objects
                    .exclude(standard_customer__in=priortized_customers_sum)
                    .aggregate(total_amount_validation=Sum('deducted_amount') / 1000000)['total_amount_validation'] or 0)
    # Add 'Others' to the chart1 data if there's any amount for other customers
    if others_amount_validation > 0:
        labels3.append('Others')
        values3.append(float(others_amount_validation))
    
    return labels3,values3

def priortized_customer_count(request):
    # Get top 8 customers by transaction count from validation table
    top_customers_validation = (om.workflow.objects
                     .values('standard_customer')
                     .annotate(transaction_count_validation=Count('id'))
                     .order_by('-transaction_count_validation')[:8])
    
    # Get top 8 customers by transaction count
    top_customers = (om.deduction_data.objects
                     .values('standard_customer')
                     .annotate(transaction_count=Count('id'))
                     .order_by('-transaction_count')[:10])
    # Get total transactions for the rest of the customers
    top_customers_ids = [customer['standard_customer'] for customer in top_customers]
    others_count = (om.deduction_data.objects
                    .exclude(standard_customer__in=top_customers_ids)
                    .aggregate(total_transactions=Count('id'))['total_transactions'] or 0)

    # Get total transactions for the rest of the customers
    top_customers_validation_id = [customer['standard_customer'] for customer in top_customers_validation]
    others_count_validation = (om.workflow.objects
                    .exclude(standard_customer__in=top_customers_validation_id)
                    .aggregate(total_transactions_validation=Count('invoice_number'))['total_transactions_validation'] or 0)
    
    # Prepare data for chart4 (Bar Chart)
    labels4 = [customer['standard_customer'] for customer in top_customers_validation]
    values4 = [customer['transaction_count_validation'] for customer in top_customers_validation]
    
    # Add 'Others' to the chart data
    if others_count > 0:
        labels4.append('Others')
        values4.append(others_count_validation)

    return labels4,values4

def invalid_valid_sku_level(request):
    #invalid and valid at sku level from validation table
    # Get total deduction, count, and invalid amounts
    deduction_validation_sku = om.validation.objects.aggregate(Sum('deducted_amount'))['deducted_amount__sum'] or 0
    deduction_count_sku = om.validation.objects.values('invoice_number').count()
    total_invalid_sku = om.validation.objects.filter(validation_status='Invalid').aggregate(Sum('invalid_amount'))['invalid_amount__sum'] or 0
    # invalid_count_validation = om.validation.objects.filter(validation_status='Invalid').count()
    invalid_count_sku =(
        om.validation.objects
        .filter(validation_status='Invalid')  # Filter for 'Invalid' status
        .values('invoice_number')  # Get unique 'invoice_number'
        .distinct()  # Ensure distinct invoice numbers
        .count()  # Count the distinct records
    )
    total_valid_sku = om.validation.objects.filter(validation_status='Valid').aggregate(Sum('valid_amount'))['valid_amount__sum'] or 0
    valid_count_sku = deduction_count_sku-invalid_count_sku

    # Convert total amounts to millions
    deduction_validation_sku = deduction_validation_sku / 1000000
    total_invalid_sku = total_invalid_sku / 1000000
    total_valid_sku = total_valid_sku / 1000000

    return deduction_validation_sku,deduction_count_sku,total_invalid_sku,invalid_count_sku,total_valid_sku,valid_count_sku

def top_carrier_deduction(request):
    # Calculate the unique customer count
    unique_carrier = om.validation.objects.values('carrier').distinct().count()
    carrier_count = om.validation.objects.values('carrier').count()

    # Fetch valid and invalid deductions grouped by carrier for amounts
    carrier_deductions_data = (om.validation.objects
                            .values('carrier')
                            .filter(~Q(carrier=""), ~Q(carrier=None))
                            .annotate(
                                total_valid_amount=Sum('valid_amount')/1000000,  # Convert to millions
                                total_invalid_amount=Sum('invalid_amount')/1000000
                            )
                            .order_by('-total_invalid_amount')
                            )

    # Prepare data for Carrier Amount Chart (Chart 5)
    carriers = [item['carrier'] for item in carrier_deductions_data]
    valid_amounts = [float(item['total_valid_amount']) for item in carrier_deductions_data]
    invalid_amounts = [float(item['total_invalid_amount']) for item in carrier_deductions_data]

    return carriers,valid_amounts,invalid_amounts,unique_carrier,carrier_count

def top_carrier_count(request):
    # Fetch valid and invalid deduction counts grouped by carrier
    carrier_deductions_count = (om.validation.objects
                                .values('carrier')
                                .filter(~Q(carrier=""), ~Q(carrier=None))
                                .annotate(
                                    valid_count=Count('id', filter=Q(validation_status='Valid')),
                                    invalid_count=Count('id', filter=Q(validation_status='Invalid'))
                                )
                                .order_by('-invalid_count')
                                )
    # Fetch valid and invalid deductions grouped by carrier for amounts
    carrier_deductions_data = (om.validation.objects
                            .values('carrier')
                            .filter(~Q(carrier=""), ~Q(carrier=None))
                            .annotate(
                                total_valid_amount=Sum('valid_amount')/1000000,  # Convert to millions
                                total_invalid_amount=Sum('invalid_amount')/1000000
                            )
                            .order_by('-total_invalid_amount')
                            )

    # Prepare data for Carrier Count Chart (Chart 6)
    carriers = [item['carrier'] for item in carrier_deductions_data]
    valid_counts = [item['valid_count'] for item in carrier_deductions_count]
    invalid_counts = [item['invalid_count'] for item in carrier_deductions_count]

    invalid_count_carrier =(
        om.validation.objects
        .filter(validation_status='Invalid')  # Filter for 'Invalid' status
        .values('carrier')  # Get unique 'invoice_number'
        .count()  # Count the distinct records
    )
    valid_count_carrier =(
        om.validation.objects
        .filter(validation_status='Valid')  # Filter for 'Invalid' status
        .values('carrier')  # Get unique 'invoice_number'
        .count()  # Count the distinct records
    )
    
    return carriers,valid_counts,invalid_counts,invalid_count_carrier,valid_count_carrier

def top_sku_deduction(request):
    # Set the number of top SKUs to display
    TOP_SKU_COUNT = 15
    unique_sku = om.validation.objects.values('sku').distinct().count()
    sku_count = om.validation.objects.values('sku').count()
    # Fetch valid and invalid deductions grouped by SKU for amounts, excluding blank SKUs
    sku_deductions_data = (
        om.validation.objects
        .filter(~Q(sku=""), ~Q(sku=None))  # Exclude blank or null SKUs
        .values('sku')
        .annotate(
            total_valid_amount=Sum('valid_amount') / 1000000,  # Convert to millions
            total_invalid_amount=Sum('invalid_amount') / 1000000
        )
        .order_by('-total_invalid_amount')[:TOP_SKU_COUNT]  # Limit to top N SKUs
    )

    # Prepare data for SKU Amount Chart7 (Top SKUs)
    skus = [item['sku'] for item in sku_deductions_data]
    valid_amounts_sku = [float(item['total_valid_amount']) for item in sku_deductions_data]
    invalid_amounts_sku = [float(item['total_invalid_amount']) for item in sku_deductions_data]

    # Fetch and sum the deductions for SKUs not in the top N
    other_sku_deductions_data = (
        om.validation.objects
        .filter(~Q(sku=""), ~Q(sku=None))  # Exclude blank or null SKUs
        .exclude(sku__in=skus)  # Exclude the top SKUs
        .aggregate(
            total_valid_amount_others=Sum('valid_amount') / 1000000,
            total_invalid_amount_others=Sum('invalid_amount') / 1000000
        )
    )

    # Append "Others" to the SKU list and the valid/invalid amounts
    skus.append('Others')
    valid_amounts_sku.append(float(other_sku_deductions_data['total_valid_amount_others'] or 0))
    invalid_amounts_sku.append(float(other_sku_deductions_data['total_invalid_amount_others'] or 0))
    
    return skus,valid_amounts_sku,invalid_amounts_sku,unique_sku,sku_count

def top_sku_count(request):
    TOP_SKU_COUNT = 15
    # Fetch valid and invalid deductions grouped by SKU for counts, excluding blank SKUs
    sku_deductions_count_data = (
        om.validation.objects
        .filter(~Q(sku=""), ~Q(sku=None))  # Exclude blank or null SKUs
        .values('sku')
        .annotate(
            total_valid_count=Count('id', filter=Q(validation_status='Valid')),  # Count valid deductions
            total_invalid_count=Count('id', filter=Q(validation_status='Invalid'))  # Count invalid deductions
        )
        .order_by('-total_invalid_count')[:TOP_SKU_COUNT]  # Limit to top N SKUs
    )
    # Fetch valid and invalid deductions grouped by SKU for amounts, excluding blank SKUs
    sku_deductions_data = (
        om.validation.objects
        .filter(~Q(sku=""), ~Q(sku=None))  # Exclude blank or null SKUs
        .values('sku')
        .annotate(
            total_valid_amount=Sum('valid_amount') / 1000000,  # Convert to millions
            total_invalid_amount=Sum('invalid_amount') / 1000000
        )
        .order_by('-total_invalid_amount')[:TOP_SKU_COUNT]  # Limit to top N SKUs
    )

    # Prepare data for SKU Count Chart8 (Top SKUs)
    skus = [item['sku'] for item in sku_deductions_data]
    valid_counts_sku = [item['total_valid_count'] for item in sku_deductions_count_data]
    invalid_counts_sku = [item['total_invalid_count'] for item in sku_deductions_count_data]

    # Fetch and sum the counts for SKUs not in the top N
    other_sku_deductions_count_data = (
        om.validation.objects
        .filter(~Q(sku=""), ~Q(sku=None))  # Exclude blank or null SKUs
        .exclude(sku__in=skus)  # Exclude the top SKUs
        .aggregate(
            total_valid_count_others=Count('id', filter=Q(validation_status='Valid')),
            total_invalid_count_others=Count('id', filter=Q(validation_status='Invalid'))
        )
    )

    # Append "Others" to the SKU counts
    valid_counts_sku.append(other_sku_deductions_count_data['total_valid_count_others'] or 0)
    invalid_counts_sku.append(other_sku_deductions_count_data['total_invalid_count_others'] or 0)

    invalid_sku_count =(
        om.validation.objects
        .filter(validation_status='Invalid')  # Filter for 'Invalid' status
        .values('sku')  # Get unique 'invoice_number'
        .count()  # Count the distinct records
    )
    valid_sku_count =(
        om.validation.objects
        .filter(validation_status='Valid')  # Filter for 'Invalid' status
        .values('sku')  # Get unique 'invoice_number'
        .count()  # Count the distinct records
    )
    
    return skus,valid_counts_sku,invalid_counts_sku,sku_deductions_count_data,invalid_sku_count,valid_sku_count

def invalid_reason_deduction(request):
    #analytics by invalid_reason starts here:
    # Fetch invalid deductions grouped by invalid_reason for amounts
    invalid_reason_data_amount = (
        om.validation.objects
        .filter(validation_status='Invalid')  # Filter for invalid deductions
        .values('invalid_reason')
        .annotate(
            total_invalid_amount=Sum('invalid_amount') / 1000000  # Convert to millions
        )
        .order_by('-total_invalid_amount')
    )
    
    # Prepare data for Invalid Reason Amount Doughnut Chart9
    invalid_reasons = [item['invalid_reason'] for item in invalid_reason_data_amount]
    invalid_amounts_by_reason = [float(item['total_invalid_amount']) for item in invalid_reason_data_amount]
    
    return invalid_reasons,invalid_amounts_by_reason

def invalid_reason_count(request):
    # Fetch invalid deductions grouped by invalid_reason for counts
    invalid_reason_data_count = (
        om.validation.objects
        .filter(validation_status='Invalid')  # Filter for invalid deductions
        .values('invalid_reason')
        .annotate(
            total_invalid_count=Count('id')  # Count the number of invalid records
        )
        .order_by('-total_invalid_count')
    )    
    # Fetch invalid deductions grouped by invalid_reason for amounts
    invalid_reason_data_amount = (
        om.validation.objects
        .filter(validation_status='Invalid')  # Filter for invalid deductions
        .values('invalid_reason')
        .annotate(
            total_invalid_amount=Sum('invalid_amount') / 1000000  # Convert to millions
        )
        .order_by('-total_invalid_amount')
    )
    
    # Prepare data for Invalid Reason Amount Doughnut Chart9
    invalid_reasons = [item['invalid_reason'] for item in invalid_reason_data_amount]
    invalid_counts_by_reason = [item['total_invalid_count'] for item in invalid_reason_data_count]
    # end of invalid reason chart data
    
    return invalid_reasons,invalid_counts_by_reason
    
#start of RCA chart data collection
def rca_chart(request):
    # Placeholder data for charts
    placeholder_labels = ['RCA', 'Invalid $', 'Valid $']
    placeholder_data = [0, 0, 0]

    # Pass data to the template
    context = {
        'datapoints_product_substitution': {
            'labels': placeholder_labels,
            'data': placeholder_data
        },
        'datapoints_combined_shipment': {
            'labels': placeholder_labels,
            'data': placeholder_data
        },
        'datapoints_order_split': {
            'labels': placeholder_labels,
            'data': placeholder_data
        },
        'datapoints_load_sequencing': {
            'labels': placeholder_labels,
            'data': placeholder_data
        },
        'datapoints_unit_of_measurement': {
            'labels': placeholder_labels,
            'data': placeholder_data
        },
        'datapoints_deducted_at_higher_price': {
            'labels': placeholder_labels,
            'data': placeholder_data
        }
    }
    return placeholder_labels,placeholder_data    
        
@login_required(login_url="/login/")
def index(request):
   labels1,values1 = top_customer_deduction_chart(request)
   labels2,values2 = top_customer_count_chart(request)
   total_deduction,deduction_count,total_invalid,invalid_count,total_valid,valid_count,unique_customer_count,unique_customer_workflow,total_deduction_validation,deduction_count_validation,total_invalid_validation,invalid_count_validation,total_valid_validation,valid_count_validation,pending_deduction_validation,pending_count_validation,pending_missing_invoice,missing_customer_sign,missing_carrier_sign,pending_subject_to_count = summary_deductions(request)
   labels3,values3 = priortized_customer_deduction(request)
   labels4,values4 = priortized_customer_count(request)
   deduction_validation_sku,deduction_count_sku,total_invalid_sku,invalid_count_sku,total_valid_sku,valid_count_sku = invalid_valid_sku_level(request)
   carriers,valid_amounts,invalid_amounts,unique_carrier,carrier_count = top_carrier_deduction(request)
   carriers,valid_counts,invalid_counts,invalid_count_carrier,valid_count_carrier = top_carrier_count(request)
   skus,valid_amounts_sku,invalid_amounts_sku,unique_sku,sku_count = top_sku_deduction(request)
   skus,valid_counts_sku,invalid_counts_sku,sku_deductions_count_data,invalid_sku_count,valid_sku_count = top_sku_count(request)
   invalid_reasons,invalid_amounts_by_reason = invalid_reason_deduction(request)
   invalid_reasons,invalid_counts_by_reason = invalid_reason_count(request)
   placeholder_labels,placeholder_data = rca_chart(request)

   context = {
        'datapoints1': {
            'labels': labels1,
            'data': values1
        },
        'datapoints2': {
            'labels': labels2,
            'data': values2
        },
        'datapoints3': {
            'labels': labels3,
            'data': values3
        },
        'datapoints4': {
            'labels': labels4,
            'data': values4
        },
        'datapoints_carrier_amount': {
            'labels': carriers,
            'valid_data': valid_amounts,
            'invalid_data': invalid_amounts
        },
        'datapoints_carrier_count': {
            'labels': carriers,
            'valid_data': valid_counts,
            'invalid_data': invalid_counts
        },
        'datapoints_sku_amount': {
            'labels': skus,
            'valid_data': valid_amounts_sku,
            'invalid_data': invalid_amounts_sku
        },
        'datapoints_sku_count': {
            'labels': skus,
            'valid_data': valid_counts_sku,
            'invalid_data': invalid_counts_sku
        },
        'datapoints_invalid_reason_amount': {
            'labels': invalid_reasons,
            'data': invalid_amounts_by_reason
        },
        'datapoints_invalid_reason_count': {
            'labels': invalid_reasons,
            'data': invalid_counts_by_reason
        },
        'datapoints_product_substitution': {
            'labels': placeholder_labels,
            'data': placeholder_data
        },
        'datapoints_combined_shipment': {
            'labels': placeholder_labels,
            'data': placeholder_data
        },
        'datapoints_order_split': {
            'labels': placeholder_labels,
            'data': placeholder_data
        },
        'datapoints_load_sequencing': {
            'labels': placeholder_labels,
            'data': placeholder_data
        },
        'datapoints_unit_of_measurement': {
            'labels': placeholder_labels,
            'data': placeholder_data
        },
        'datapoints_deducted_at_higher_price': {
            'labels': placeholder_labels,
            'data': placeholder_data
        },
        'total_deduction': total_deduction,
        'deduction_count': deduction_count,
        'total_invalid': total_invalid,
        'invalid_count': invalid_count,
        'total_valid': total_valid,
        'valid_count': valid_count,
        'unique_customer_count': unique_customer_count,  # Add the unique customer count here
        'unique_customer_workflow': unique_customer_workflow, # Add the unique customer count here
        'total_deduction_validation': total_deduction_validation,
        'deduction_count_validation': deduction_count_validation,
        'total_invalid_validation': total_invalid_validation,
        'invalid_count_validation': invalid_count_validation,
        'total_valid_validation': total_valid_validation,
        'valid_count_validation': valid_count_validation,
        'unique_carrier': unique_carrier,
        'carrier_count': carrier_count,
        'invalid_count_carrier': invalid_count_carrier,
        'valid_count_carrier': valid_count_carrier,
        'unique_sku': unique_sku,
        'sku_count': sku_count,
        'sku_deductions_count_data': sku_deductions_count_data,
        'invalid_sku_count': invalid_sku_count,
        'valid_sku_count': valid_sku_count,
        'deduction_validation_sku': deduction_validation_sku,
        'deduction_count_sku': deduction_count_sku,
        'total_invalid_sku': total_invalid_sku,
        'invalid_count_sku': invalid_count_sku,
        'total_valid_sku': total_valid_sku,
        'valid_count_sku': valid_count_sku,
        'pending_deduction_validation': pending_deduction_validation,
        'pending_count_validation':pending_count_validation,
        'pending_missing_invoice': pending_missing_invoice,
        'missing_customer_sign': missing_customer_sign,
        'missing_carrier_sign': missing_carrier_sign,
        'pending_subject_to_count': pending_subject_to_count,

   }
   return render(request, 'home.html',context)

# @login_required(login_url="/login/")
# def index(request):
#     # Query to get the sum of deduction_amount for each standard_customer
#     data = (om.deduction_data.objects
#             .values('standard_customer')
#             .annotate(total_amount=Sum('deduction_amount')/1000000)
#             .order_by('-total_amount')[:10])  # Order by descending and limit to top 8
    
#     # Prepare data for chart1 (Bar Chart)
#     labels1 = [item['standard_customer'] for item in data]
#     values1 = [float(item['total_amount']) for item in data]

#     # Get the total deduction amount for the rest of the customers (others)
#     top_customers_sum = [item['standard_customer'] for item in data]
#     others_amount = (om.deduction_data.objects
#                      .exclude(standard_customer__in=top_customers_sum)
#                      .aggregate(total_amount=Sum('deduction_amount') / 1000000)['total_amount'] or 0)
#     # Add 'Others' to the chart1 data if there's any amount for other customers
#     if others_amount > 0:
#         labels1.append('Others')
#         values1.append(float(others_amount))
    
#     # Get top 8 customers by transaction count
#     top_customers = (om.deduction_data.objects
#                      .values('standard_customer')
#                      .annotate(transaction_count=Count('id'))
#                      .order_by('-transaction_count')[:10])
    
#     # Get total transactions for the rest of the customers
#     top_customers_ids = [customer['standard_customer'] for customer in top_customers]
#     others_count = (om.deduction_data.objects
#                     .exclude(standard_customer__in=top_customers_ids)
#                     .aggregate(total_transactions=Count('id'))['total_transactions'] or 0)
    
#     # Prepare data for chart2 (Bar Chart)
#     labels2 = [customer['standard_customer'] for customer in top_customers]
#     values2 = [customer['transaction_count'] for customer in top_customers]
    
#     # Add 'Others' to the chart data
#     if others_count > 0:
#         labels2.append('Others')
#         values2.append(others_count)
    
#     # Calculate the unique customer count
#     unique_customer_count = om.deduction_data.objects.values('standard_customer').distinct().count()

#     # Get total deduction, count, and invalid amounts
#     total_deduction = om.workflow.objects.aggregate(Sum('deducted_amount'))['deducted_amount__sum'] or 0
#     deduction_count = om.workflow.objects.count()
#     total_invalid = om.validation.objects.filter(validation_status='Invalid').aggregate(Sum('invalid_amount'))['invalid_amount__sum'] or 0
#     invalid_count = om.validation.objects.filter(validation_status='Invalid').count()
#     total_valid = om.validation.objects.filter(validation_status='Valid').aggregate(Sum('valid_amount'))['valid_amount__sum'] or 0
#     valid_count = om.validation.objects.filter(validation_status='Valid').count()
    
#     # Convert total amounts to millions
#     total_deduction = total_deduction / 1000000
#     total_invalid = total_invalid / 1000000
#     total_valid = total_valid / 1000000

    

#     # Calculate the unique customer count
#     unique_customer_workflow = om.workflow.objects.values('standard_customer').distinct().count()
    
#     # Get total deduction, count, and invalid amounts
#     # total_deduction_validation = om.workflow.objects.aggregate(Sum('deducted_amount'))['deducted_amount__sum'] or 0
    
#     deduction_count_validation = om.workflow.objects.values('invoice_number').count()
#     pending_deduction_validation = om.workflow.objects.filter(validation_status='Pending Validation').aggregate(Sum('deducted_amount'))['deducted_amount__sum'] or 0
#     pending_count_validation = om.workflow.objects.filter(validation_status='Pending Validation').count()
#     total_invalid_validation = om.workflow.objects.filter(validation_status='Invalid').aggregate(Sum('invalid_amount'))['invalid_amount__sum'] or 0
#     # invalid_count_validation = om.validation.objects.filter(validation_status='Invalid').count()
#     invalid_count_validation =(
#         om.workflow.objects
#         .filter(validation_status='Invalid')  # Filter for 'Invalid' status
#         .values('invoice_number')  # Get unique 'invoice_number'
#         .distinct()  # Ensure distinct invoice numbers
#         .count()  # Count the distinct records
#     )
#     total_valid_validation = om.workflow.objects.filter(validation_status='Valid').aggregate(Sum('valid_amount'))['valid_amount__sum'] or 0
#     valid_count_validation = deduction_count_validation-invalid_count_validation - pending_count_validation
#     total_deduction_validation = total_invalid_validation+total_valid_validation+pending_deduction_validation

#     # pending validation split
#     pending_missing_invoice = om.workflow.objects.filter(invalid_reason='Missing Invoice Data').aggregate(Sum('deducted_amount'))['deducted_amount__sum'] or 0
#     missing_customer_sign = om.workflow.objects.filter(invalid_reason='Customer sign is missing on POD').aggregate(Sum('deducted_amount'))['deducted_amount__sum'] or 0
#     missing_carrier_sign = om.workflow.objects.filter(invalid_reason='Carrier sign is missing on POD').aggregate(Sum('deducted_amount'))['deducted_amount__sum'] or 0
#     pending_subject_to_count = om.workflow.objects.filter(invalid_reason='POD is subject to count').aggregate(Sum('deducted_amount'))['deducted_amount__sum'] or 0

#     # Convert total amounts to millions
#     total_deduction_validation = total_deduction_validation / 1000000
#     total_invalid_validation = total_invalid_validation / 1000000
#     total_valid_validation = total_valid_validation / 1000000
#     pending_deduction_validation=pending_deduction_validation/1000000
#     pending_missing_invoice=pending_missing_invoice/1000000
#     missing_customer_sign=missing_customer_sign/1000000
#     missing_carrier_sign=missing_carrier_sign/1000000
#     pending_subject_to_count=pending_subject_to_count/1000000
    
#     # Query to get the sum of deduction_amount for each standard_customer
#     validation_data = (om.workflow.objects
#             .values('standard_customer')
#             .annotate(total_amount_validation=Sum('deducted_amount')/1000000)
#             .order_by('-total_amount_validation')[:8])  # Order by descending and limit to top 8
    
#     # Prepare data for chart3 (Bar Chart)
#     labels3 = [item['standard_customer'] for item in validation_data]
#     values3 = [float(item['total_amount_validation']) for item in validation_data]

#     # Get the total deduction amount for the rest of the customers (others)
#     priortized_customers_sum = [item['standard_customer'] for item in validation_data]
#     others_amount_validation = (om.validation.objects
#                      .exclude(standard_customer__in=priortized_customers_sum)
#                      .aggregate(total_amount_validation=Sum('deducted_amount') / 1000000)['total_amount_validation'] or 0)
#     # Add 'Others' to the chart1 data if there's any amount for other customers
#     if others_amount_validation > 0:
#         labels3.append('Others')
#         values3.append(float(others_amount_validation))

#     # Get top 8 customers by transaction count from validation table
#     top_customers_validation = (om.workflow.objects
#                      .values('standard_customer')
#                      .annotate(transaction_count_validation=Count('id'))
#                      .order_by('-transaction_count_validation')[:8])
    
#     # Get total transactions for the rest of the customers
#     top_customers_validation_id = [customer['standard_customer'] for customer in top_customers_validation]
#     others_count_validation = (om.workflow.objects
#                     .exclude(standard_customer__in=top_customers_validation_id)
#                     .aggregate(total_transactions_validation=Count('invoice_number'))['total_transactions_validation'] or 0)
    
#     # Prepare data for chart4 (Bar Chart)
#     labels4 = [customer['standard_customer'] for customer in top_customers_validation]
#     values4 = [customer['transaction_count_validation'] for customer in top_customers_validation]
    
#     # Add 'Others' to the chart data
#     if others_count > 0:
#         labels4.append('Others')
#         values4.append(others_count_validation)


#     #invalid and valid at sku level from validation table
#     # Get total deduction, count, and invalid amounts
#     deduction_validation_sku = om.validation.objects.aggregate(Sum('deducted_amount'))['deducted_amount__sum'] or 0
#     deduction_count_sku = om.validation.objects.values('invoice_number').count()
#     total_invalid_sku = om.validation.objects.filter(validation_status='Invalid').aggregate(Sum('invalid_amount'))['invalid_amount__sum'] or 0
#     # invalid_count_validation = om.validation.objects.filter(validation_status='Invalid').count()
#     invalid_count_sku =(
#         om.validation.objects
#         .filter(validation_status='Invalid')  # Filter for 'Invalid' status
#         .values('invoice_number')  # Get unique 'invoice_number'
#         .distinct()  # Ensure distinct invoice numbers
#         .count()  # Count the distinct records
#     )
#     total_valid_sku = om.validation.objects.filter(validation_status='Valid').aggregate(Sum('valid_amount'))['valid_amount__sum'] or 0
#     valid_count_sku = deduction_count_sku-invalid_count_sku

#     # Convert total amounts to millions
#     deduction_validation_sku = deduction_validation_sku / 1000000
#     total_invalid_sku = total_invalid_sku / 1000000
#     total_valid_sku = total_valid_sku / 1000000

#     # Calculate the unique customer count
#     unique_carrier = om.validation.objects.values('carrier').distinct().count()
#     carrier_count = om.validation.objects.values('carrier').count()

#     # Fetch valid and invalid deductions grouped by carrier for amounts
#     carrier_deductions_data = (om.validation.objects
#                             .values('carrier')
#                             .filter(~Q(carrier=""), ~Q(carrier=None))
#                             .annotate(
#                                 total_valid_amount=Sum('valid_amount')/1000000,  # Convert to millions
#                                 total_invalid_amount=Sum('invalid_amount')/1000000
#                             )
#                             .order_by('-total_invalid_amount')
#                             )

#     # Prepare data for Carrier Amount Chart (Chart 5)
#     carriers = [item['carrier'] for item in carrier_deductions_data]
#     valid_amounts = [float(item['total_valid_amount']) for item in carrier_deductions_data]
#     invalid_amounts = [float(item['total_invalid_amount']) for item in carrier_deductions_data]

#     # Fetch valid and invalid deduction counts grouped by carrier
#     carrier_deductions_count = (om.validation.objects
#                                 .values('carrier')
#                                 .filter(~Q(carrier=""), ~Q(carrier=None))
#                                 .annotate(
#                                     valid_count=Count('id', filter=Q(validation_status='Valid')),
#                                     invalid_count=Count('id', filter=Q(validation_status='Invalid'))
#                                 )
#                                 .order_by('-invalid_count')
#                                 )

#     # Prepare data for Carrier Count Chart (Chart 6)
#     valid_counts = [item['valid_count'] for item in carrier_deductions_count]
#     invalid_counts = [item['invalid_count'] for item in carrier_deductions_count]

#     invalid_count_carrier =(
#         om.validation.objects
#         .filter(validation_status='Invalid')  # Filter for 'Invalid' status
#         .values('carrier')  # Get unique 'invoice_number'
#         .count()  # Count the distinct records
#     )
#     valid_count_carrier =(
#         om.validation.objects
#         .filter(validation_status='Valid')  # Filter for 'Invalid' status
#         .values('carrier')  # Get unique 'invoice_number'
#         .count()  # Count the distinct records
#     )


#     # Set the number of top SKUs to display
#     TOP_SKU_COUNT = 15
#     unique_sku = om.validation.objects.values('sku').distinct().count()
#     sku_count = om.validation.objects.values('sku').count()
#     # Fetch valid and invalid deductions grouped by SKU for amounts, excluding blank SKUs
#     sku_deductions_data = (
#         om.validation.objects
#         .filter(~Q(sku=""), ~Q(sku=None))  # Exclude blank or null SKUs
#         .values('sku')
#         .annotate(
#             total_valid_amount=Sum('valid_amount') / 1000000,  # Convert to millions
#             total_invalid_amount=Sum('invalid_amount') / 1000000
#         )
#         .order_by('-total_invalid_amount')[:TOP_SKU_COUNT]  # Limit to top N SKUs
#     )

#     # Prepare data for SKU Amount Chart7 (Top SKUs)
#     skus = [item['sku'] for item in sku_deductions_data]
#     valid_amounts_sku = [float(item['total_valid_amount']) for item in sku_deductions_data]
#     invalid_amounts_sku = [float(item['total_invalid_amount']) for item in sku_deductions_data]

#     # Fetch and sum the deductions for SKUs not in the top N
#     other_sku_deductions_data = (
#         om.validation.objects
#         .filter(~Q(sku=""), ~Q(sku=None))  # Exclude blank or null SKUs
#         .exclude(sku__in=skus)  # Exclude the top SKUs
#         .aggregate(
#             total_valid_amount_others=Sum('valid_amount') / 1000000,
#             total_invalid_amount_others=Sum('invalid_amount') / 1000000
#         )
#     )

#     # Append "Others" to the SKU list and the valid/invalid amounts
#     skus.append('Others')
#     valid_amounts_sku.append(float(other_sku_deductions_data['total_valid_amount_others'] or 0))
#     invalid_amounts_sku.append(float(other_sku_deductions_data['total_invalid_amount_others'] or 0))

#     # Fetch valid and invalid deductions grouped by SKU for counts, excluding blank SKUs
#     sku_deductions_count_data = (
#         om.validation.objects
#         .filter(~Q(sku=""), ~Q(sku=None))  # Exclude blank or null SKUs
#         .values('sku')
#         .annotate(
#             total_valid_count=Count('id', filter=Q(validation_status='Valid')),  # Count valid deductions
#             total_invalid_count=Count('id', filter=Q(validation_status='Invalid'))  # Count invalid deductions
#         )
#         .order_by('-total_invalid_count')[:TOP_SKU_COUNT]  # Limit to top N SKUs
#     )

#     # Prepare data for SKU Count Chart8 (Top SKUs)
#     valid_counts_sku = [item['total_valid_count'] for item in sku_deductions_count_data]
#     invalid_counts_sku = [item['total_invalid_count'] for item in sku_deductions_count_data]

#     # Fetch and sum the counts for SKUs not in the top N
#     other_sku_deductions_count_data = (
#         om.validation.objects
#         .filter(~Q(sku=""), ~Q(sku=None))  # Exclude blank or null SKUs
#         .exclude(sku__in=skus)  # Exclude the top SKUs
#         .aggregate(
#             total_valid_count_others=Count('id', filter=Q(validation_status='Valid')),
#             total_invalid_count_others=Count('id', filter=Q(validation_status='Invalid'))
#         )
#     )

#     # Append "Others" to the SKU counts
#     valid_counts_sku.append(other_sku_deductions_count_data['total_valid_count_others'] or 0)
#     invalid_counts_sku.append(other_sku_deductions_count_data['total_invalid_count_others'] or 0)

#     invalid_sku_count =(
#         om.validation.objects
#         .filter(validation_status='Invalid')  # Filter for 'Invalid' status
#         .values('sku')  # Get unique 'invoice_number'
#         .count()  # Count the distinct records
#     )
#     valid_sku_count =(
#         om.validation.objects
#         .filter(validation_status='Valid')  # Filter for 'Invalid' status
#         .values('sku')  # Get unique 'invoice_number'
#         .count()  # Count the distinct records
#     )


#     #analytics by invalid_reason starts here:
#     # Fetch invalid deductions grouped by invalid_reason for amounts
#     invalid_reason_data_amount = (
#         om.validation.objects
#         .filter(validation_status='Invalid')  # Filter for invalid deductions
#         .values('invalid_reason')
#         .annotate(
#             total_invalid_amount=Sum('invalid_amount') / 1000000  # Convert to millions
#         )
#         .order_by('-total_invalid_amount')
#     )

#     # Fetch invalid deductions grouped by invalid_reason for counts
#     invalid_reason_data_count = (
#         om.validation.objects
#         .filter(validation_status='Invalid')  # Filter for invalid deductions
#         .values('invalid_reason')
#         .annotate(
#             total_invalid_count=Count('id')  # Count the number of invalid records
#         )
#         .order_by('-total_invalid_count')
#     )

#     # Prepare data for Invalid Reason Amount Doughnut Chart9
#     invalid_reasons = [item['invalid_reason'] for item in invalid_reason_data_amount]
#     invalid_amounts_by_reason = [float(item['total_invalid_amount']) for item in invalid_reason_data_amount]

#     # Prepare data for Invalid Reason Count Doughnut Chart9
#     invalid_counts_by_reason = [item['total_invalid_count'] for item in invalid_reason_data_count]
#     # end of invalid reason chart data

#     #start of RCA chart data collection

#     # Placeholder data for charts
#     placeholder_labels = ['RCA', 'Invalid $', 'Valid $']
#     placeholder_data = [0, 0, 0]

    
#     # Pass data to the template
#     context = {
#         'datapoints1': {
#             'labels': labels1,
#             'data': values1
#         },
#         'datapoints2': {
#             'labels': labels2,
#             'data': values2
#         },
#         'datapoints3': {
#             'labels': labels3,
#             'data': values3
#         },
#         'datapoints4': {
#             'labels': labels4,
#             'data': values4
#         },
#          'datapoints_carrier_amount': {
#             'labels': carriers,
#             'valid_data': valid_amounts,
#             'invalid_data': invalid_amounts
#         },
#          'datapoints_carrier_count': {
#             'labels': carriers,
#             'valid_data': valid_counts,
#             'invalid_data': invalid_counts
#         },
#          'datapoints_sku_amount': {
#             'labels': skus,
#             'valid_data': valid_amounts_sku,
#             'invalid_data': invalid_amounts_sku
#         },
#          'datapoints_sku_count': {
#             'labels': skus,
#             'valid_data': valid_counts_sku,
#             'invalid_data': invalid_counts_sku
#         },
#         'datapoints_invalid_reason_amount': {
#             'labels': invalid_reasons,
#             'data': invalid_amounts_by_reason
#         },
#         'datapoints_invalid_reason_count': {
#             'labels': invalid_reasons,
#             'data': invalid_counts_by_reason
#         },
#         'datapoints_product_substitution': {
#             'labels': placeholder_labels,
#             'data': placeholder_data
#         },
#         'datapoints_combined_shipment': {
#             'labels': placeholder_labels,
#             'data': placeholder_data
#         },
#         'datapoints_order_split': {
#             'labels': placeholder_labels,
#             'data': placeholder_data
#         },
#         'datapoints_load_sequencing': {
#             'labels': placeholder_labels,
#             'data': placeholder_data
#         },
#         'datapoints_unit_of_measurement': {
#             'labels': placeholder_labels,
#             'data': placeholder_data
#         },
#         'datapoints_deducted_at_higher_price': {
#             'labels': placeholder_labels,
#             'data': placeholder_data
#         },
#         'total_deduction': total_deduction,
#         'deduction_count': deduction_count,
#         'total_invalid': total_invalid,
#         'invalid_count': invalid_count,
#         'total_valid': total_valid,
#         'valid_count': valid_count,
#         'unique_customer_count': unique_customer_count,  # Add the unique customer count here
#         'unique_customer_workflow': unique_customer_workflow, # Add the unique customer count here
#         'total_deduction_validation': total_deduction_validation,
#         'deduction_count_validation': deduction_count_validation,
#         'total_invalid_validation': total_invalid_validation,
#         'invalid_count_validation': invalid_count_validation,
#         'total_valid_validation': total_valid_validation,
#         'valid_count_validation': valid_count_validation,
#         'unique_carrier': unique_carrier,
#         'carrier_count': carrier_count,
#         'invalid_count_carrier': invalid_count_carrier,
#         'valid_count_carrier': valid_count_carrier,
#         'unique_sku': unique_sku,
#         'sku_count': sku_count,
#         'sku_deductions_count_data': sku_deductions_count_data,
#         'invalid_sku_count': invalid_sku_count,
#         'valid_sku_count': valid_sku_count,
#         'deduction_validation_sku': deduction_validation_sku,
#         'deduction_count_sku': deduction_count_sku,
#         'total_invalid_sku': total_invalid_sku,
#         'invalid_count_sku': invalid_count_sku,
#         'total_valid_sku': total_valid_sku,
#         'valid_count_sku': valid_count_sku,
#         'pending_deduction_validation': pending_deduction_validation,
#         'pending_count_validation':pending_count_validation,
#         'pending_missing_invoice': pending_missing_invoice,
#         'missing_customer_sign': missing_customer_sign,
#         'missing_carrier_sign': missing_carrier_sign,
#         'pending_subject_to_count': pending_subject_to_count,

#     }
#     return render(request, 'home.html', context)



@login_required(login_url="/login/")
def backup_upload(request):
    
    categories = Category.objects.values_list('category', flat=True).distinct()
    retailers = Category.objects.values_list('retailer', flat=True).distinct()
    subcategories = Category.objects.values_list('subcategories', flat=True).distinct()
    # print(categories,retailers,subcategories)
    context = {'categories': categories,
        'retailers': retailers,
        'subcategories': subcategories}
    
    if request.method == 'POST':
        retailer_option = request.POST.get('retailer')
        selected_option = request.POST.get('subcategories')
        excel_file = request.FILES.get('excel_file')  # Use get() method with a default value
        pdf_file = request.FILES.get('pdf_file')
        # file = request.FILES.get('file')

        request.session['retailer_option'] = retailer_option

       
        
        if selected_option == 'OSD Data' and (retailer_option == 'None' or retailer_option == 'BD'):
            cv.deductions_upload(request, excel_file, context)
        
        elif selected_option == 'OSD Backup' and (retailer_option == 'None' or retailer_option == 'BD'):
            cv.backup_upload(request, excel_file, context)
        
        elif selected_option == 'Invoice Data' and (retailer_option == 'None' or retailer_option == 'BD'):
            invoice_upload(request, excel_file, context)
        
        elif selected_option == 'POD' and (retailer_option == 'None' or retailer_option == 'BD'):
            cv.pod_detail_upload(request, excel_file, context)

        elif selected_option == 'Freight Data' and (retailer_option == 'None' or retailer_option == 'BD'):
            fv.deductions_upload (request, excel_file, context)

        elif selected_option == 'Freight Backup' and (retailer_option == 'None' or retailer_option == 'BD'):
            fv.backup_upload(request, excel_file, context)

        elif selected_option == 'EDI Master' and (retailer_option == 'None' or retailer_option == 'BD'):
            fv.edi_master_upload(request, excel_file, context)

        elif selected_option == 'EDI Actual' and (retailer_option == 'None' or retailer_option == 'BD'):
            fv.edi_actual_upload(request, excel_file, context)

        elif selected_option == 'Freight Communication' and (retailer_option == 'None' or retailer_option == 'BD'):
            fv.freight_communication_upload(request, excel_file, context)

        elif selected_option == 'Pricing Data' and (retailer_option == 'None' or retailer_option == 'BD'):
            pv.deductions_upload(request, excel_file, context)

        elif selected_option == 'Pricing Backup' and (retailer_option == 'None' or retailer_option == 'BD'):
            pv.backup_upload(request, excel_file, context)
        
        elif selected_option == 'Price Change Data' and (retailer_option == 'None' or retailer_option == 'BD'):
            pv.price_change_upload(request, excel_file, context)

        elif selected_option == 'Promotions Data' and (retailer_option == 'None' or retailer_option == 'BD'):
                    prv.amazon_remit_upload(request, excel_file, context)

        elif selected_option == 'Promotions Backup' and (retailer_option == 'None' or retailer_option == 'BD'):
                    prv.amazon_promo_backup_upload(request, excel_file, context)

        elif selected_option == 'Contract' and (retailer_option == 'None' or retailer_option == 'BD'):
                    prv.amazon_agreement_upload(request, excel_file, context)

        elif selected_option == 'PO Data' and (retailer_option == 'None' or retailer_option == 'BD'):
                    prv.amazon_po_upload(request, excel_file, context)

    return render(request, 'backup_upload.html', context)
    

@login_required(login_url="/login/")
def upload_status(request):
   
    date_field = []
    #setup pagination
    data = Paginator(UploadedCSV.objects.all(),20)
    page = request.GET.get('page')
    page_obj = data.get_page(page)
    fields = UploadedCSV._meta.fields

    excluded_fields = []
    return render(request, 'upload_status.html', {'page_obj': page_obj, 'data': data, 'fields': fields, 'date_field': date_field, 'excluded_fields': excluded_fields})

def parse_time_or_none(time_str):
    try:
        # Parse the time string in the format '6:45:18 AM'
        parsed_time = datetime.strptime(time_str, '%I:%M:%S %p').time()
        return parsed_time
    except ValueError:
        # Handle invalid time format by returning None
        return None



@login_required(login_url="/login/")
def invoice_upload(request, excel_file=None, context={}):
    try:
        if excel_file:
            # Load the Excel data into a pandas DataFrame
            df = pd.read_csv(excel_file, dtype={'invoice_number': str,'sku': str, 'lane':str})
            start_time = timezone.now()

            # Set initial status
            current_status = 'started'
            total_rows = df.shape[0]
            instances = []

            # Define a function to convert NaN to default values
            def get_value(value, default=0):
                return default if pd.isna(value) else value

            # Iterate over each row in the DataFrame and validate the data
            for _, row in df.iterrows():
                try:
                    # Extract fields as per the model
                    inv_sku = row['concat'] if 'concat' in row else ''
                    invoice_number = row['invoice_number'] if 'invoice_number' in row else ''
                    invoice_date = row['invoice_date']
                    if pd.notnull(invoice_date):
                        try:
                            invoice_date = datetime.strptime(invoice_date, '%m/%d/%Y').date()
                        except ValueError:
                            print(f"Error parsing invoice_date: {invoice_date}")
                            invoice_date = None
                    else:
                        invoice_date = None
                    
                    sku = row['sku'] if 'sku' in row else ''
                    billed_qty = clean_value(row['billed_qty'], 0)
                    gross_price = row['gross_price']
                    if gross_price is None or gross_price == '':
                        gross_price = 0.0
                    else:
                        gross_price = convert_to_decimal_V2(gross_price)
                        if gross_price is None or gross_price != gross_price:
                            gross_price = 0.0
                    oi_deal = clean_value(row['oi_deal'], 0.0)
                    promo_allowance = clean_value(row['promo_allowance'], 0.0)
                    cash_discount = clean_value(row['cash_discount'], 0.0)
                    freight_amount = clean_value(row['freight_amount'], 0.0)
                    others = clean_value(row['others'], 0.0)
                    net_price = row['net_price']
                    if net_price is None or net_price == '':
                        net_price = 0.0
                    else:
                        net_price = convert_to_decimal_V2(net_price)
                        if net_price is None or net_price != net_price:
                            net_price = 0.0
                    gross_price_per_qty = clean_value(
                        row['gross_price_per_qty'], 0.0)
                    net_price_per_qty = clean_value(
                        row['net_price_per_qty'], 0.0)
                    fuel_allowance = clean_value(row['fuel_allowance'], 0.0)
                    lane = row['lane'] if 'lane' in row else ''
                    
                    freight_rate = clean_value(row['freight_rate'], 0.0)
                    
                    gross_weight = row['gross_weight']
                    if gross_weight is None or gross_weight == '':
                        gross_weight = 0.0
                    else:
                        gross_weight = convert_to_decimal_V2(gross_weight)
                        if gross_weight is None or gross_weight != gross_weight:
                            gross_weight = 0.0

                    total_freight = row['total_freight']
                    if total_freight is None or total_freight == '':
                        total_freight = 0.0
                    else:
                        total_freight = convert_to_decimal_V2(total_freight)
                        if total_freight is None or total_freight != total_freight:
                            total_freight = 0.0

                    order_number = row['order_number'] if 'order_number' in row else ''
                    bol = row['bol'] if 'bol' in row else ''
                    carrier = row['carrier'] if 'carrier' in row else ''

                    # Check if the record already exists in the model
                    if invoice_data.objects.filter(invoice_number=invoice_number,sku=sku, billed_qty=billed_qty).exists():
                        continue

                    # Create an instance of the model
                    instance = invoice_data(
                        inv_sku=inv_sku,
                        invoice_number=invoice_number,
                        invoice_date=invoice_date,
                        sku=sku,
                        billed_qty=billed_qty,
                        gross_price=gross_price,
                        oi_deal=oi_deal,
                        promo_allowance=promo_allowance,
                        cash_discount=cash_discount,
                        freight_amount=freight_amount,
                        others=others,
                        net_price=net_price,
                        gross_price_per_qty=gross_price_per_qty,
                        net_price_per_qty=net_price_per_qty,
                        fuel_allowance=fuel_allowance,
                        lane=lane,
                        freight_rate=freight_rate,
                        gross_weight=gross_weight,
                        total_freight=total_freight,
                        order_number=order_number,
                        bol=bol,
                        carrier=carrier
                    )
                    instances.append(instance)

                except ValueError as e:
                    print(f"ValueError for row {row}: {e}")
                except Exception as e:
                    print(f"Unexpected error for row {row}: {e}")

            # Bulk insert the instances
            if instances:
                invoice_data.objects.bulk_create(instances)

            end_time = timezone.now()
            total_time = end_time - start_time

            # Update upload status
            current_status = 'completed'
            request.session['upload_status'] = 'success'

            # Log the upload details
            uploaded_csv = mm.UploadedCSV.objects.create(
                user=request.user,
                file=excel_file,
                num_rows=df.shape[0],
                start_time=start_time,
                end_time=end_time,
                total_time=total_time,
                current_status=current_status
            )
            return redirect('backup_upload')

        else:
            context['error'] = 'No Excel file was uploaded.'

    except pd.errors.EmptyDataError:
        context['error'] = 'The uploaded file is empty.'

    except pd.errors.ParserError as e:
        context['error'] = f'Error parsing the CSV file: {e}'

    except ValidationError as e:
        context['error'] = f'Validation error: {e}'

    except Exception as e:
        context['error'] = f'An unexpected error occurred: {e}'

    return render(request, 'backup_upload.html', context)

@login_required(login_url="/login/")
def invoice_view(request):
    date_field = []
    excluded_fields = ['id', 'inv_sku','carrier']
    # Setup pagination
    data = Paginator(invoice_data.objects.all(), 10)
    page = request.GET.get('page')
    page_obj = data.get_page(page)
    fields = invoice_data._meta.fields
    field_names = [
        field.name for field in fields if field.name not in excluded_fields]
    print(field_names)

    return render(request, 'invoice_data.html', {'date_field': date_field, 'page_obj': page_obj, 'data': data, 'field_names': field_names})


@login_required(login_url="/login/")
def reporting(request):
    if request.method == 'POST':
        reporting_option = request.POST.get('reporting_option')

        # Determine sorting parameters from the request
        sort_by = request.GET.get('sort_by', 'invoice_number')  # Default sorting by invoice_number
        sort_order = request.GET.get('sort_order', 'asc')  # Default order is ascending
        
        # Set ordering direction
        if sort_order == 'asc':
            order_by = sort_by
        else:
            order_by = f'-{sort_by}'

        if reporting_option == 'billback':
            # Fetch all invalid invoices and sort by the selected field
            invalid_invoices = om.validation.objects.filter(validation_status='Invalid').values(
                'invoice_number', 'standard_customer'
            ).distinct().order_by(order_by)

            return render(request, 'billback_package.html', {
                'invalid_invoices': invalid_invoices,
                'sort_by': sort_by,
                'sort_order': sort_order,
            })

    return render(request, 'reporting.html')


def find_file(directory, invoice_number):
    """Helper function to find a file containing the invoice number in its name."""
    for filename in os.listdir(directory):
        if invoice_number in filename:
            return os.path.join(directory, filename)
    return None


def generate_billback_document(invoice_data):
    """Generate billback template content using provided invoice data."""
    context = {
        'deduction_amount': invoice_data['deduction_amount'],
        'invalid_amount': invoice_data['invalid_amount'],
        'invoice_number': invoice_data['invoice_number'],
        'po_number': invoice_data['po_number'],
        'account': invoice_data['account'],
        'customer_name': invoice_data['customer_name']
    }
    # Use Django template system to render the billback document
    return render_to_string('billback_template.txt', context)


def create_billback_package(request):
    if request.method == 'POST':
        selected_invoices = request.POST.getlist('selected_invoices')

        if not selected_invoices:
            return HttpResponse("No invoices selected.", status=400)

        # Directory paths for pod, invoice, and backup
        pod_dir = os.path.join(settings.BASE_DIR, 'Uploads', 'pod')
        invoice_dir = os.path.join(settings.BASE_DIR, 'Uploads', 'invoice')
        backup_dir = os.path.join(settings.BASE_DIR, 'Uploads', 'backup')

        # Create ZIP archive in memory
        zip_filename = 'billback_package.zip'
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for invoice_number in selected_invoices:
                # Create a folder in the ZIP for each invoice number
                folder_name = f'{invoice_number}/'
                
                # Fetch invoice data from the database
                invoice_instance = get_object_or_404(om.deduction_data, invoice_number=invoice_number, validation_status='Invalid')
                # Fetch related data from other tables
                po_instance = mm.invoice_data.objects.filter(invoice_number=invoice_instance.invoice_number).first()
                invoice_data = {
                    'deduction_amount': invoice_instance.deduction_amount,
                    'invalid_amount': invoice_instance.invalid_amount,
                    'invoice_number': invoice_instance.invoice_number,
                    # 'po_number': invoice_instance.po_number,
                    'po_number': po_instance.order_number if po_instance else 'Not Available',
                    'account': invoice_instance.customer_account,
                    'customer_name': invoice_instance.standard_customer
                }

                # Generate and add the billback document to the ZIP
                billback_content = generate_billback_document(invoice_data)
                zip_file.writestr(os.path.join(folder_name, 'billback_document.txt'), billback_content)

                # Find and add POD, Invoice, and Backup files
                pod_file = find_file(pod_dir, invoice_number)
                invoice_file = find_file(invoice_dir, invoice_number)
                backup_file = find_file(backup_dir, invoice_number)

                if pod_file:
                    zip_file.write(pod_file, os.path.join(folder_name, os.path.basename(pod_file)))
                if invoice_file:
                    zip_file.write(invoice_file, os.path.join(folder_name, os.path.basename(invoice_file)))
                if backup_file:
                    zip_file.write(backup_file, os.path.join(folder_name, os.path.basename(backup_file)))

        zip_buffer.seek(0)

        # Return the ZIP file for download
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename={zip_filename}'

        return response
