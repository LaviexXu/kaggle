from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile
# Register your models here.


class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

