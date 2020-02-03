from django.urls import path

from members.views import MemberViewSet, MemberListForAccount

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

member_list_for_account = MemberListForAccount.as_view({
    'get': 'list',
})

urlpatterns = [
    path('api/v1/members/bulk-create/', bulk_create, name='bulk_create'),
    path('api/v1/members/list/', member_list, name='member_list'),
    path('api/v1/members/by-id/<str:member_id>/', member_detail, name='member_detail_id'),
    path('api/v1/members/by-phone/<str:phone_number>/', member_detail, name='member_detail_phone'),
    path('api/v1/members/by-mrn/<int:client_member_id>/', member_detail, name='member_detail_mrn'),

    path('api/v1/accounts/<str:pk>/member-list/', member_list_for_account, name='member_list_for_account'),

]
