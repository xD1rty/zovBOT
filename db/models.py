from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)
    tg_id = fields.IntField()
    username = fields.TextField()

    def __str__(self):
        return self.username


class Group(Model):
    id = fields.IntField(pk=True)
    organizer = fields.ForeignKeyField('models.User', related_name='organized_groups')
    participants = fields.ManyToManyField('models.User', related_name='groups', through='group_user')
    invite_code = fields.TextField()


class Zov(Model):
    id = fields.IntField(pk=True)
    starttime = fields.DatetimeField(auto_now_add=True)
    group = fields.ForeignKeyField('models.Group', related_name='zovs')
    remindtime = fields.IntField(default=5)
    secret_meet_code = fields.TextField()