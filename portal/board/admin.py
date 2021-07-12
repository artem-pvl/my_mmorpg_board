from django.contrib import admin

from .models import Category, Ad, Reply


# Register your models here.

admin.site.register(Category)
admin.site.register(Ad)
admin.site.register(Reply)
