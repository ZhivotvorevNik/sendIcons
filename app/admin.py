from django.contrib import admin

# Register your models here.

from .models import Zone
from .models import Service

admin.site.register(Zone)
admin.site.register(Service)