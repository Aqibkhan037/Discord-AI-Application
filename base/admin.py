from django.contrib import admin

# Register your models here.
from .models import Rooms,Topic,Message

admin.site.register(Rooms)
admin.site.register(Topic)
admin.site.register(Message)

