from django.urls import path
from . import views

urlpatterns = [
    path('', views.associate_list, name='associate_list'),
    path('add/', views.add_associate, name='add_associate'),
]
