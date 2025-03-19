from django.contrib import admin
from django.urls import path, include
from osd import views
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path('osd_deductions/', views.deductions_view, name='deductions_view'),
    path('osd_backup/', views.backup_view, name='backup_view'),   
    path('uploads/', views.upload_pod, name='upload_pod'),
    path('pdf_list/', views.pdf_list, name='pdf_list'),
    path('pod_update/<int:pod_id>/', views.update_pod_details, name='update_pod_details'),
    path('transform_osd_data/', views.transform_osd_data, name='transform_osd_data'),
    path('osd_validation_view/', views.osd_validation_view, name='osd_validation_view'),
    path('delete_osd_data/', views.delete_osd_data, name='delete_osd_data'),
    path('workflow/', views.workflow_view, name='workflow_view'),
    path('refresh_workflow/', views.refresh_workflow, name='refresh_workflow'),
    path('workflow/edit/<int:workflow_id>/', views.edit_workflow, name='edit_workflow'),
    # path('create_billback_package/', views.create_billback_package, name='create_billback_package'),
    path('create-billback-package/', views.create_billback_package_view, name='create_billback_package'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.UPLOADS_URL, document_root=settings.UPLOADS_ROOT)