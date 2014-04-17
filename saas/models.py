from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

class Tenant(models.Model):
    company = models.CharField(unique=true)
    username  = models.CharField(unique=true)
    password = models.CharField(unique=true)
    addproject = models.BooleanField(initial=false)
    addRequirements = models.BooleanField(initial=false)
    modifyProjectStatus = models.BooleanField(initial=false)
    viewReqStatus = models.BooleanField(initial=false)
    viewProjectsManager = models.BooleanField(initial=false)
    modReqStatus = models.BooleanField(initial=false)
    viewAssignedReqs = models.BooleanField(initial=false)
    








