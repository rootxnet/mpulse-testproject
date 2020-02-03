"""
mpulsedemo URL Configuration
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/members/', include('members.urls', namespace='members')),
    path('api/v1/accounts/', include('accounts.urls', namespace='accounts')),
]
