from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils import FieldTracker


class MyUser(AbstractUser):
    state = models.CharField(max_length=225, blank=True)
    city = models.CharField(max_length=225, blank=True)
    zipcode = models.CharField(max_length=224, blank=True)
    tracker = FieldTracker()  # track all the fields in the model

    zipcode_tracker = FieldTracker(fields=['zipcode'])  # to track particular Fileds

    class Meta:
        db_table = 'auth_user'
