from django.db import models
from django.contrib.auth.models import User


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

    def __unicode__(self):
        return self.company




class Manager(models.Model):
    tenant = models.ForeignKey(Tenant)
    firstName = models.CharField(max_length = 128)
    lastName = models.CharField(max_length = 128)
    username = models.CharField(max_length = 128, unique = True)
    password = models.CharField(max_length = 128, unique = True)

    def __unicode__(self):
        return self.firstName

class Worker(models.Model):
    tenant = models.ForeignKey(Tenant)
    manager = models.ForeignKey(Manager)
    firstName = models.CharField(max_length = 128)
    lastName = models.CharField(max_length = 128)
    username = models.CharField(max_length = 128, unique = True)
    password = models.CharField(max_length = 128, unique = True)

    def __unicode__(self):
        return self.firstName


class Requirement(models.Model):
    tenant = models.ForeignKey(Tenant)
    worker = models.ForeignKey(Worker)
   # project = models.ForeignKey(Project)
    manager = models.ForeignKey(Manager)
    timeReq = models.IntegerField(default=0)
    description = models.CharField(max_length=300)
    reqType = models.CharField(max_length=300)

    def __unicode__(self):
        return self.timeReq


class Project(models.Model):
    tenant = models.ForeignKey(Tenant)
    manager = models.ForeignKey(Manager)
    worker = models.ManyToManyField(Worker, verbose_name = "list of workers")
    requirement = models.ManyToManyField(Requirement, verbose_name = "list of requirments")
    name = models.CharField(max_length = 128, unique=True)
    startDate = models.DateField()
    endDate = models.DateField()
    status = models.BooleanField()

    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username









