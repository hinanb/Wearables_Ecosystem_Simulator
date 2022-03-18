from django.contrib import admin
from .models import Wearable, Sensor, Sensor_Values, Configuration
# Register your models here.

admin.site.register(Wearable)

admin.site.register( Sensor)
admin.site.register( Sensor_Values)
admin.site.register( Configuration)
