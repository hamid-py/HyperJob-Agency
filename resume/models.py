from django.contrib.auth.models import User
from django.db import models
from django.db.models import IntegerField, CharField, ForeignKey, CASCADE


class Resume(models.Model):
    description = CharField(max_length=1024)
    author = ForeignKey(User, on_delete=CASCADE)


    def __str__(self):
        return self.description
