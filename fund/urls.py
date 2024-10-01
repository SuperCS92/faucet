
from django.urls import path
from . import views

urlpatterns = [
    path('fund/', views.fund, name='fund'),
    path('stats/', views.transaction_stats, name='transaction_stats'),  # URL for retrieving stats
]