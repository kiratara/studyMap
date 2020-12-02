from django.contrib import admin

from map import models

admin.site.register(models.Topic)
admin.site.register(models.SubTopic)
admin.site.register(models.Note)
