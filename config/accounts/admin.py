from django.contrib import admin
from .models import User


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'no',
        'user_id',
        'cname',
        'user_pw',
        'user_phone',
        'user_email',
        'user_date',
        'user_status'
    )