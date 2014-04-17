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
    company = models.CharField(max_length = 128,unique=True)
    username  = models.CharField(max_length = 128,unique=True)
    password = models.CharField(max_length = 128,unique=True)
    addproject = models.BooleanField()
    addRequirements = models.BooleanField()
    modifyProjectStatus = models.BooleanField()
    viewReqStatus = models.BooleanField()
    viewProjectsManager = models.BooleanField()
    modReqStatus = models.BooleanField()
    viewAssignedReqs = models.BooleanField()
    








