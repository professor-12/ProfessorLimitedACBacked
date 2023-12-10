from django.contrib import admin
from .models import Chat, Profile, Contacts, Group, GroupChat
# Register your models here.
admin.site.register(Chat)
admin.site.register(Group)
admin.site.register(Profile)
admin.site.register(Contacts)
admin.site.register(GroupChat)
