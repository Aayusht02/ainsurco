from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.clients_list, name='clients_list'),
    path('<int:pk>/', views.clients_detail, name='clients_detail'),
    path('<int:pk>/edit/', views.clients_edit, name='clients_edit'),
    path('add-client/', views.add_client, name='add_client'),
    
]

