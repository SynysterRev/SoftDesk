from rest_framework import viewsets, status
from rest_framework.response import Response

from projects.models import Project, Contributor, Issue, Comment
from projects.serializers import (ProjectListSerializer, ProjectDetailSerializer,
                                  IssueListSerializer, IssueDetailSerializer)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectDetailSerializer
    queryset = Project.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        project = Project.objects.get(id=response.data['id'])
        user = request.user
        Contributor.objects.get_or_create(user=user, project=project)
        for contributor in project.contributors.all():
                Contributor.objects.get_or_create(user=contributor, project=project)
        return Response(response.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return super().get_serializer_class()

class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueDetailSerializer
    queryset = Issue.objects.all().select_related('project')

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        serializer.save(author=self.request.user, project=project)

    def get_serializer_class(self):
        if self.action == "list":
            return IssueListSerializer
        return super().get_serializer_class()

class CommentViewSet(viewsets.ModelViewSet):
    pass
    # serializer_class = CommentDetailSerializer
    #
    # def get_queryset(self):
    #     return Comment.objects.filter(issue=self.kwargs['issue_pk'])
    #
    # def perform_create(self, serializer):
    #     issue = Issue.objects.get(pk=self.kwargs['issue_pk'])
    #     serializer.save(author=self.request.user, issue=issue)
    #
    # def get_serializer_class(self):
    #     if self.action == "list":
    #         return CommentListSerializer
    #     return super().get_serializer_class()
