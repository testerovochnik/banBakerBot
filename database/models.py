from config import DB_PATH

from peewee import (Model, SqliteDatabase,
                    PrimaryKeyField, TextField, DateTimeField, CharField, DateField,
                    BooleanField, IntegerField, ForeignKeyField, AutoField)


db = SqliteDatabase(DB_PATH)


class BaseModel(Model):

    class Meta:
        database = db


class Users(BaseModel):
    user_id: PrimaryKeyField = PrimaryKeyField(primary_key=True)
    username: TextField = TextField()
    is_banned: bool = BooleanField(default=False)


class Notes(BaseModel):
    id: AutoField = AutoField(primary_key=True)
    title: TextField = TextField()
    content: TextField = TextField()
    format_type = CharField(choices=['markdown', 'html'], default='markdown')
    date: DateField = DateField()
    created_at: DateTimeField = DateTimeField()
    updated_at: DateTimeField = DateTimeField(null=True)
    created_by: ForeignKeyField = ForeignKeyField(Users, backref="creators")
    updated_by: ForeignKeyField = ForeignKeyField(Users, backref="updaters", null=True)
    views: int = IntegerField(default=0)
    is_deleted: bool = BooleanField(default=False)


class Comments(BaseModel):
    id: AutoField = AutoField(primary_key=True)
    comment: TextField = TextField()
    created_at: DateTimeField = DateTimeField()
    created_by: ForeignKeyField = ForeignKeyField(Users, backref="users")
    note_id = ForeignKeyField(Notes, backref="notes")
    is_moderated: bool = BooleanField(default=False)
    moderated_at: DateTimeField = DateTimeField(null=True)
    moderated_by: ForeignKeyField = ForeignKeyField(Users, backref="moderators", null=True)
    is_approved: bool = BooleanField(default=False)
