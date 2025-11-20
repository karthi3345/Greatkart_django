from django.contrib import admin
from django.contrib.auth.admin import UserAdmin





class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'user_name', 'last_login', 'date_joined', 'is_active')
    search_fields = ('email', 'first_name', 'user_name')

    readonly_fields = ('date_joined', 'last_login','password')

    ordering = ('date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    list_display_links=('email','first_name')

# Register your models here.
from .models import Account
admin.site.register(Account,AccountAdmin)

# ✔️ What is this?

# You created a custom admin class for your Account model.
# This class controls how your model looks inside Django Admin panel.

# ✔️ What list_display does?

# list_display tells Django:

# “Which columns should appear on the admin list page?”

# When you open Django Admin → Accounts, you will see a table like:

# | email | first_name | user_name | last_login | date_joined | is_active |

# These columns come from list_display.

# ✔️ Example (admin list table)
# email              first_name   username   last_login     date_joined   is_active
# -----------------------------------------------------------------------------------
# user1@gmail.com     Karthik      karthik     2025-11-10     2025-11-01       ✔️
# user2@gmail.com     Raj          raj123      2025-11-11     2025-11-02       ❌

# ✔️ Why do we extend UserAdmin?

# Because:

# UserAdmin already knows how to handle:

# password

# permissions

# groups

# login

# last login

# is_staff

# is_superuser

# fields display

# fieldsets
# So your custom user gets all admin features automatically.

# ✔️ Summary (super simple)
# Part	Meaning
# class AccountAdmin(UserAdmin)	You are customizing how Account appears in Django Admin
# list_display=(...)	Shows these columns in admin list view

# If you want, I can explain fieldsets, search_fields, ordering also.