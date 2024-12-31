from django.conf import settings
from django.urls import path
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path('', views.leads_list, name='leads_list'),
    path('<int:pk>/', views.leads_detail, name='leads_detail'),
    path('dashboard/leads/<int:id>/edit/', views.leads_edit, name='leads_edit'),
    path('add-lead/', views.add_lead, name='add_lead'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
