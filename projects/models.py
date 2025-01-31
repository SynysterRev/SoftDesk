from django.db import models

from django.conf import settings

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
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects")
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
