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
# from amazon import views
from django.conf import settings
from django.conf.urls.static import static
from main import views as mv


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-panel/', mv.admin_panel, name='admin_panel'),
    path('user_details/<str:username>/', mv.user_details, name='user_details'),      
    path('profile/', mv.profile, name='profile'),
    path('change-password/', mv.CustomPasswordChangeView.as_view(), name='password_change'), 
    path('', include('osd.urls')), 
    path('', include('freight.urls')),
    path('', include('main.urls')), 
    path('', include('pricing.urls')), 
    path('', include('promotions.urls')), 
    path('login/', mv.user_login, name='user_login'),
    path('logout/', mv.user_logout, name='user_logout'),
    path('', mv.index, name='index'),
    path('backup_upload/', mv.backup_upload, name='backup_upload'),
    path('upload_status', mv.upload_status, name='upload_status'),     
# ]
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 
# Serve media files during development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
