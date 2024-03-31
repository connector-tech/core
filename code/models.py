from tortoise import fields, models

from code.utils import pwd_context


class Common(models.Model):
    id = fields.UUIDField(pk=True)  # noqa
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class User(Common):
    username = fields.CharField(max_length=255, null=True, unique=True)
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    age = fields.IntField(null=True)
    bio = fields.TextField(null=True)
    interests = fields.ManyToManyField(
        'models.Interest',
        related_name='users',
        through='user_interests',
    )
    password = fields.CharField(max_length=255)

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def check_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)

    class Meta:
        table = 'users'


class UserInterests(models.Model):
    user = fields.ForeignKeyField('models.User', related_name='user_interests')
    interest = fields.ForeignKeyField('models.Interest', related_name='user_interests')

    class Meta:
        table = 'user_interests'
        unique_together = ('user', 'interest')


class Interest(Common):
    name = fields.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        table = 'interests'
