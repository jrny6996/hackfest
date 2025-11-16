from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='jonny'),
    path('url-generate/', views.generate_url, name='null'),
    path('customer-refresh/', views.consolidate_customer, name='pain'),
    path('timed-data/', views.timed_transaction, name='pain'),
    
]