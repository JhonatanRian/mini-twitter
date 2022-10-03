from django.db import models


# Create your models here.

class Base(models.Model):
    datetime_created = models.DateTimeField(auto_now_add=True)
    update = models.DateField(auto_now=True)

    class Meta:
        abstract = True