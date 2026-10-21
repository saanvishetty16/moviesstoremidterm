from django.db import models
from django.contrib.auth.models import User

class TopCustomer(User):
    class Meta:
        proxy = True
        verbose_name = "Top Customer"
        verbose_name_plural = "Top Customer:"