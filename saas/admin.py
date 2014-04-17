from django.contrib import admin

# Register your models here.
from saas.models import Category, Page, Tenant

admin.site.register(Category)
admin.site.register(Page)
admin.site.register(Tenant)