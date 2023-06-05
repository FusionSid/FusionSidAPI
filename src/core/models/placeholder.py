from tortoise import fields
from tortoise.models import Model


class User(Model):
    """
    Example model for a user from the database
    """

    id = fields.BigIntField(pk=True, null=False)
    username = fields.CharField(32, unique=True, null=False)
    password = fields.TextField(null=False)

    class Meta:
        table = "users"
