from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, RecogData, ConversationData, Classroom, Lecture, RoomData
# Register your models here.

admin.site.register(CustomUser, UserAdmin)
admin.site.register(RecogData)
admin.site.register(ConversationData)
admin.site.register(Classroom)
admin.site.register(Lecture)
admin.site.register(RoomData)
# admin.site.register(CustomUser)
