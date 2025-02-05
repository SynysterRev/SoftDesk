import uuid

from django.conf import settings
from django.db import models


class Project(models.Model):
    class ProjectType(models.TextChoices):
        BACKEND = "back-end", "Back-end"
        FRONTEND = "front-end", "Front-end"
        IOS = "iOS", "iOS"
        ANDROID = "android", "Android"


    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.CharField(choices=ProjectType, default=ProjectType.BACKEND,
                            max_length=10)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name="projects")
    created_time = models.DateTimeField(auto_now_add=True)
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                          through="Contributor",
                                          related_name="contributions")


class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="user_contributions")
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name="project_contributors")
    created_time = models.DateTimeField(auto_now_add=True)


class Issue(models.Model):
    class IssueTag(models.TextChoices):
        BUG = "bug", "Bug"
        FEATURE = "feature", "Feature"
        TASK = "task", "Task"


    class IssuePriority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"


    class IssueStatus(models.TextChoices):
        TODO = "to do", "To Do"
        IN_PROGRESS = "in progress", "In Progress"
        FINISHED = "finished", "Finished"


    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(choices=IssueStatus, default=IssueStatus.TODO,
                              max_length=20)
    priority = models.CharField(choices=IssuePriority, default=IssuePriority.HIGH,
                                max_length=20)
    tag = models.CharField(choices=IssueTag, default=IssueTag.TASK, max_length=20)
    created_time = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    related_name="assigned_issues")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name="issues_created")
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name="issues")


class Comment(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                            unique=True)
    description = models.TextField(blank=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE,
                              related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name="omments_created")
    created_time = models.DateTimeField(auto_now_add=True)
