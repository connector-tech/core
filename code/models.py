import datetime
from enum import StrEnum

from tortoise import fields, models

from code.utils import pwd_context


class Common(models.Model):
    id = fields.UUIDField(pk=True)  # noqa
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class User(Common):
    class GenderEnum(StrEnum):
        MALE = 'MALE'
        FEMALE = 'FEMALE'

    username = fields.CharField(max_length=255, null=True, unique=True)
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    birth_date = fields.DateField(null=True)
    bio = fields.TextField(null=True)
    gender = fields.CharEnumField(GenderEnum, default=GenderEnum.MALE, null=True)
    password = fields.CharField(max_length=255)
    photos = fields.JSONField(default=[])
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
    is_chat_started = fields.BooleanField(default=False)

    class Meta:
        table = 'user_social'
        unique_together = [('viewer_id', 'user_id')]
        indexes = [('viewer_id', 'user_id')]


class Message(Common):
    user = fields.ForeignKeyField('models.User', related_name='messages')
    chat = fields.ForeignKeyField('models.Chat', related_name='messages')
    text = fields.TextField()
    is_read = fields.BooleanField(default=False)

    class Meta:
        table = 'messages'
        indexes = ['user_id', 'created_at']


class Chat(Common):
    user_1 = fields.ForeignKeyField('models.User', related_name='chats_1')
    user_2 = fields.ForeignKeyField('models.User', related_name='chats_2')
    first_message = fields.DatetimeField(auto_now_add=True)
    last_message = fields.DatetimeField(null=True)

    class Meta:
        table = 'chats'
        unique_together = [('user_1_id', 'user_2_id')]
        indexes = ['user_1_id', 'user_2_id', 'created_at']


class QuestionnaireQuestion(Common):
    text = fields.TextField()

    class Meta:
        table = 'questionnaire_questions'


class UserQuestionnaireAnswer(Common):
    user = fields.ForeignKeyField('models.User', related_name='questionnaires')
    question = fields.ForeignKeyField('models.QuestionnaireQuestion', related_name='answers')
    answer = fields.TextField()

    class Meta:
        table = 'user_questionnaire_answers'
        indexes = ['user_id']


class UserSimilarity(Common):
    user_1 = fields.ForeignKeyField('models.User', related_name='similar_users_1', index=True)
    user_2 = fields.ForeignKeyField('models.User', related_name='similar_users_2', index=True)
    similarity = fields.FloatField(index=True)

    class Meta:
        table = 'user_similarity'
        unique_together = [('user_1_id', 'user_2_id')]
