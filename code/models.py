import datetime

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
    birth_date = fields.DateField(null=True)
    bio = fields.TextField(null=True)
    password = fields.CharField(max_length=255)
    interests = fields.ManyToManyField(
        'models.Interest',
        related_name='users',
        through='user_interests',
    )

    def __str__(self):
        return self.username

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    @property
    def age(self) -> int | None:
        if not self.birth_date:
            return None
        return (datetime.date.today() - self.birth_date).days // 365

    def check_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)

    class Meta:
        table = 'users'


class Interest(Common):
    name = fields.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        table = 'interests'


class UserSocial(Common):
    viewer = fields.ForeignKeyField('models.User', related_name='viewed')
    user = fields.ForeignKeyField('models.User', related_name='viewers')
    is_liked = fields.BooleanField(default=False)

    class Meta:
        table = 'user_social'
        indexes = [('viewer_id', 'user_id')]
