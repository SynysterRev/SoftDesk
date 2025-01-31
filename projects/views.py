from rest_framework import viewsets

from projects.models import Project, Contributor
from projects.serializers import (ProjectListSerializer, ProjectDetailSerializer)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectDetailSerializer
    queryset = Project.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=user, project=project)
        for contributor in project.contributors.all():
            if not Contributor.objects.filter(user=user, project=project).exists():
                Contributor.objects.create(user=contributor, project=project)

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return super().get_serializer_class()
