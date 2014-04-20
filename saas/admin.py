from django.contrib import admin

# Register your models here.
from saas.models import Category, Page, Manager, Worker, Requirement, Project, UserProfile

admin.site.register(Category)
admin.site.register(Page)
admin.site.register(Manager)
admin.site.register(Worker)
admin.site.register(Requirement)
admin.site.register(Project)
admin.site.register(UserProfile)