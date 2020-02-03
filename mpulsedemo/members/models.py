import uuid

from django.db import models

from accounts.models import Account
from meta.models import BaseModel


class Member(BaseModel):
    """
    This model contains member data
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    member_id = models.PositiveIntegerField(unique=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=30)

    account = models.ForeignKey(Account, related_name="members", on_delete=models.CASCADE)
    client_member_id = models.PositiveIntegerField()

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        unique_together = [
            ["account", "client_member_id"],
            ["account", "phone_number"]
        ]
