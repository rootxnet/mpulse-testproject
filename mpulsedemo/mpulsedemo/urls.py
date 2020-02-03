"""
mpulsedemo URL Configuration
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('members.urls', namespace='members')),
    path('', include('accounts.urls', namespace='accounts')),
]
