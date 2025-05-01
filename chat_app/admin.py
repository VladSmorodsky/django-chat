from django.contrib import admin

from chat_app.models import User, Chat, Message


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_superuser')
    search_fields = ('email',)

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass