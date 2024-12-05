from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core.views import index
from userprofile.views import signup

urlpatterns = [

    path('', index, name='index'),
    path('dashboard/clients/', include('client.urls')),
    path('dashboard/leads/', include('lead.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('sign-up/', signup, name='signup'),
    path('log-in/', views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('log-out/', views.LogoutView.as_view(template_name='userprofile/logout.html'), name='logout'),
    path('admin/', admin.site.urls),
    
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
