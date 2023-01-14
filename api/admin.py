from django.contrib import admin
from .models import PlanChoices,PhoneNumber, UserInfo

# Register your models here.


admin.site.register(PlanChoices)
admin.site.register(PhoneNumber)
admin.site.register(UserInfo)
