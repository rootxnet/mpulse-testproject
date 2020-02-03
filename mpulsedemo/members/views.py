from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Member
from .serializers import MemberSerializer, BulkMemberCreateSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    lookup_fields = ["member_id", "phone_number", "client_member_id"]

    def get_object(self):
        """
        Overriding get_object to allow for multiple alternative lookup fields so we can query
        single objects by more than one
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_field_in_use = set(self.lookup_fields) & set(self.kwargs.keys())

        assert lookup_field_in_use, (
            'Expected view {} to be called with one of URL keyword arguments '
            'named {}. Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.'.format(
                self.__class__.__name__, ", ".join(self.lookup_fields)
            )
        )
        lookup_field_in_use = lookup_field_in_use.pop()

        filter_kwargs = {lookup_field_in_use: self.kwargs[lookup_field_in_use]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def bulk_create(self, request, *args, **kwargs):
        """
        Creates bulk db insert from CSV file
        """
        serializer = BulkMemberCreateSerializer(data=[request.data, ], many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
