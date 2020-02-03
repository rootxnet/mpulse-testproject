from django.urls import path

from accounts.views import AccountViewSet

app_name = "accounts"

account_list = AccountViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

account_detail = AccountViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

urlpatterns = [
    path('api/v1/accounts/list/', account_list, name='account_list'),
    path('api/v1/accounts/<str:pk>/', account_detail, name='account_detail'),
]
