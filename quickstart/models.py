from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
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

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ('created',)