from django.contrib import admin

from app.models import SystemSetting, GPIOPin, Shutter, Job

# Register your models here.
admin.site.register([SystemSetting, GPIOPin, Shutter, Job])

