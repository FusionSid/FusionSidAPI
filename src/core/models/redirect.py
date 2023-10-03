from tortoise import fields
from tortoise.models import Model


class Redirect(Model):
    """
    Model for redirect record
    """

    slug = fields.CharField(10, pk=True, unique=True, null=False)
    url = fields.CharField(256, null=False)
    created_at = fields.DatetimeField(auto_now_add=True, null=False)
    views = fields.IntField()
    last_edited = fields.DatetimeField(auto_now=True)
    expires_at = fields.DatetimeField(null=True)

    class Meta:
        table = "redirects"
