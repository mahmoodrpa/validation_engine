"""
URL configuration for validation_engine project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from promotions import views

urlpatterns = [
    path('promo_data/', views.amazon_remittance, name='promo_data'),
    path('amazon_promo_backup/', views.promo_backup, name='amazon_promo_backup'),
    path('amazonpo_data/', views.amazonpo_data, name='amazonpo_data'),
    path('amazon_contract_data/', views.amazon_contract, name='amazon_contract_data'),
    path('transform_promotions_data/', views.transform, name='transform_promotions_data'),
    path('delete_data/', views.delete_data, name='delete_data'),
    path('promo_validation/', views.promo_validation, name='promo_validation'),
    

]
