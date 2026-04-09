from django.contrib import admin

from accounts.models import Profile , Product

class profileadmin(admin.ModelAdmin):
    list_display=('role','user')


admin.site.register(Profile,profileadmin)
admin.site.register(Product)