from tortoise import fields
from tortoise.models import Model


class File(Model):
    """
    Model for file record
    """

    slug = fields.CharField(10, pk=True, unique=True, null=False)
    data = fields.BinaryField(null=False)
    created_at = fields.DatetimeField(auto_now_add=True, null=False)
    downloads = fields.IntField()
    last_edited = fields.DatetimeField(auto_now=True)
    expires_at = fields.DatetimeField(null=True)

    class Meta:
        table = "files"
