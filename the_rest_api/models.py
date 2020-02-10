from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)
    description = models.TextField(null=False)
    completed = models.BooleanField(default=False, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Action(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    note = models.TextField(null=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)