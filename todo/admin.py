from django.contrib import admin
from .models import Task, User, SharedTask, Friend, Tag 

# Register your models here.
admin.site.register(User)
admin.site.register(Task)
admin.site.register(SharedTask)
admin.site.register(Friend)
admin.site.register(Tag)
