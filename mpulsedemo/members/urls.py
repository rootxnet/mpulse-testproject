from django.urls import path

from members.views import MemberViewSet

app_name = "members"

bulk_create = MemberViewSet.as_view({
    'post': 'bulk_create'
})

member_list = MemberViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

member_detail = MemberViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

urlpatterns = [
    path('bulk-create/', bulk_create, name='bulk_create'),
    path('list/', member_list, name='member_list'),
    path('by-id/<str:member_id>/', member_detail, name='member_detail_id'),
    path('by-phone/<str:phone_number>/', member_detail, name='member_detail_phone'),
    path('by-mrn/<int:client_member_id>/', member_detail, name='member_detail_mrn'),
]
