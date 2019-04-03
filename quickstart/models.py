from django.db import models
from django.core.validators import RegexValidator


class User(models.Model):
    user_id = models.CharField(max_length=20, unique=True,
                               validators=[RegexValidator(regex=r'^[A-Za-z0-9]+$',
                                                          message="there is invalid char in used",
                                                          )]
                               )

    password = models.CharField(max_length=20,
                                validators=[RegexValidator(regex=r'^[A-Za-z0-9]+$',
                                                           message="there is invalid char in used",
                                                           )]
                                )

    nickname = models.TextField(max_length=30, null=True)
    comment = models.TextField(max_length=100, null=True)
