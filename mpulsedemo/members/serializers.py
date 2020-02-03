import csv

import io
from rest_framework import serializers

from accounts.models import Account
from .models import Member

# source -> target
CSV_FIELD_MAPPING = {
    "id": "member_id",
}
BULK_INSERT_BATCH_SIZE = 200


class MemberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="member_id")
    account_id = serializers.IntegerField(source="account.id")

    class Meta:
        model = Member
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "account_id",
            "client_member_id",
        ]

    def create(self, validated_data):
        account = validated_data.pop("account")
        print(account)
        validated_data["account"], _ = Account.objects.get_or_create(
            id=account["id"]
        )
        return super().create(validated_data)


class BulkMemberCreateListSeralizer(serializers.ListSerializer):
    _all = None

    def _rename_key(self, dict, old_key, new_key):
        dict[new_key] = dict[old_key]
        del dict[old_key]
        return dict

    def _handle_csv_data(self, csv_file):
        csv_file = io.TextIOWrapper(csv_file)  # python 3 only
        csv_file.seek(0)
        return csv.DictReader(csv_file)

    def create(self, validated_data):
        objects = []
        for item in validated_data:
            csv_file = item.pop("csv_file")
            self._all = self._handle_csv_data(csv_file=csv_file)

            # apply field mapping in case CSV field names are not aligned with model fields
            for old_key, new_key in CSV_FIELD_MAPPING.items():
                self._all = [
                    self._rename_key(y, old_key, new_key) for y in self._all
                ]

            # represent CSV entries as Member objects for insertion
            bulk_prep = [Member(**m) for m in self._all]

            # this is a hack which creates mock Account objects before Members are inserted
            bulk_account_prep = []
            for n in bulk_prep:
                bulk_account_prep.append(
                    Account(id=n.account_id)
                )

            # create mock accounts for members
            accounts = Account.objects.bulk_create(
                bulk_account_prep,
                batch_size=BULK_INSERT_BATCH_SIZE,
                ignore_conflicts=True
            )

            # insert members in bulk, BULK_INSERT_BATCH_SIZE defines number of
            # members in a single transaction
            objs = Member.objects.bulk_create(
                bulk_prep,
                batch_size=BULK_INSERT_BATCH_SIZE,
                ignore_conflicts=True  # requires postgres > 9.5
            )

            objects.extend(objs)
        return objects

    def to_representation(self, data):
        _all_ids = [row[CSV_FIELD_MAPPING["id"]] for row in self._all]

        # find instances only, unfortunately data does not provide a way to find out which
        # objects failed to insert without making a lot of queries
        _created_ids = Member.objects.filter(
            id__in=[l.id for l in data]
        ).values_list("member_id", flat=True)

        failed_ids = set(_created_ids) ^ set(map(int, _all_ids))
        failed = filter(lambda y: int(y["id"]) not in _created_ids, self._all)
        # revert field mapping
        for old_key, new_key in CSV_FIELD_MAPPING.items():
            self._all = [
                self._rename_key(y, old_key=new_key, new_key=old_key) for y in self._all
            ]

        return [
            ("success", super().to_representation(data)),
            ("failed_ids",
             failed_ids
             ),
            ("failed",
             failed
             )
        ]


class BulkMemberCreateSerializer(serializers.ModelSerializer):
    csv_file = serializers.FileField(write_only=True)
    id = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = [
            "csv_file",

            "id",
            "first_name",
            "last_name",
            "phone_number",
            "account_id",
            "client_member_id",
        ]

        read_only_fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "account_id",
            "client_member_id",
        ]

        list_serializer_class = BulkMemberCreateListSeralizer

    def get_id(self, obj):
        """
        Use member_id instead of real pk for compatibility with API/CSV
        """
        return int(obj.member_id)