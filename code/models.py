from tortoise import fields, models


class Common(models.Model):
    id = fields.UUIDField(pk=True)  # noqa
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class User(Common):
    username = fields.CharField(max_length=255)
    full_name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255)
    age = fields.IntField()
    password = fields.CharField(max_length=255)

    def __str__(self):
        return self.username

    class Meta:
        table = 'users'
