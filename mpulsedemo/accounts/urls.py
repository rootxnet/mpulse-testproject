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
    path('list/', account_list, name='account_list'),
    path('<str:pk>/', account_detail, name='account_detail'),
]
