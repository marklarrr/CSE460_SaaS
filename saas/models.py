from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    addproject = models.BooleanField(default = False)
    addRequirements = models.BooleanField(default = False)
    modifyProjectStatus = models.BooleanField(default = False)
    viewReqStatus = models.BooleanField(default = False)
    viewProjectsManager = models.BooleanField(default = False)
    modReqStatus = models.BooleanField(default = False)
    viewAssignedReqs = models.BooleanField(default = False)
    websiteRank = models.IntegerField(default=1)

    def __unicode__(self):
        return self.user.username

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

class Manager(models.Model):
    user = models.OneToOneField(User)
    tenant = models.ForeignKey(UserProfile)
    firstName = models.CharField(max_length = 128)
    lastName = models.CharField(max_length = 128)
    websiteRank = models.IntegerField(default=2)

    def __unicode__(self):
        return self.firstName

class Worker(models.Model):
    user = models.OneToOneField(User)
    tenant = models.ForeignKey(UserProfile)
    manager = models.ForeignKey(Manager)
    firstName = models.CharField(max_length = 128)
    lastName = models.CharField(max_length = 128)
    websiteRank = models.IntegerField(default=3)

    def __unicode__(self):
        return self.firstName


class Requirement(models.Model):
    tenant = models.ForeignKey(UserProfile)
    worker = models.ForeignKey(Worker)
   # project = models.ForeignKey(Project)
    manager = models.ForeignKey(Manager)
    timeReq = models.IntegerField(default=0)
    description = models.CharField(max_length=300)
    reqType = models.CharField(max_length=300)

    def __unicode__(self):
        return self.description

class Project(models.Model):

    tenant = models.ForeignKey(UserProfile)

    manager = models.ForeignKey(Manager)
    worker = models.ManyToManyField(Worker, verbose_name = "list of workers")
    requirement = models.ManyToManyField(Requirement, verbose_name = "list of requirments")
    name = models.CharField(max_length = 128, unique=True)
    startDate = models.DateField()
    endDate = models.DateField()
    status = models.BooleanField()

    def __unicode__(self):
        return self.name