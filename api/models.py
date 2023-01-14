from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

PLAN_CHOICES = (
    ('Bronze', 500),
    ('Silver', 750),
    ('Gold', 1500)
)


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=500, default="")
    if_logged = models.BooleanField(default=False)

    # def __str__(self):
    #     return user.user.username



class PhoneNumber(models.Model):
    phone_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=11)
    primary_number = models.BooleanField(default=False)

    def __str__(self):
        return self.contact


class PlanChoices(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE)
    plan = models.CharField(choices=PLAN_CHOICES, max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.plan

    # def count_duration(self):
    #     timeduration = 0
    #     if not self.updated_at:
    #         timeduration = self.created_at - datetime.date.now()
    #     else: 
    #         timeduration = self.updated_at - datetime.date.now()
    #     return timeduration









