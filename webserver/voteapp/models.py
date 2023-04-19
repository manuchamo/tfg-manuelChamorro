from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from enum import IntEnum
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from django.utils.text import slugify


class VoteType(IntEnum):
    """
        Define la enumeracion Voto
    """
    CATS = 1
    DOGS = 2
    TIE = 3

    @classmethod
    def choices(cls):
        """
            return: Pares valor, nombre de la enumeracion
        """
        return [(int(x.value), str(x.name)) for x in cls]


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='voter')
    date = models.DateField(blank=True, null=True)
    voteType = models.IntegerField(blank=False, choices=VoteType.choices(), default=VoteType.TIE)

    def __str__(self):
        return '[ ' + str(self.date) + ' ]' + ' -> ' + str(self.user) + ' vota a: ' + str(self.voteType)

    def save(self, *args, **kwargs):
        if self.date is None:
            self.date = datetime.datetime.now()
        super(Vote, self).save(*args, **kwargs)