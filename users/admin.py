from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):

    list_display = ("id", "username", "can_data_be_shared", "age", "can_be_contacted")


admin.site.register(User, UserAdmin)
