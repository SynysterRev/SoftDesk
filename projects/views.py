from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from projects.models import Project, Contributor, Issue, Comment
from projects.permissions import IsAuthorOrContributor
from projects.serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    IssueListSerializer,
    IssueDetailSerializer,
    CommentListSerializer,
    CommentDetailSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated, (IsAdminUser | IsAuthorOrContributor)]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        project = Project.objects.get(id=response.data["id"])
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

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Project.objects.all()
        queryset = Project.objects.filter(
            Q(author=user) | Q(project_contributors__user=user)
        ).distinct()
        return queryset


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated, (IsAdminUser | IsAuthorOrContributor)]

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs["project_pk"])

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs["project_pk"])
        assigned_to = serializer.validated_data.get("assigned_to")
        if assigned_to and not Contributor.objects.filter(project=project,
                                   user=assigned_to).exists():
            raise ValidationError({"assigned_to": "L'utilisateur doit être un contributeur du projet."})

        serializer.save(author=self.request.user, project=project)

    def get_serializer_class(self):
        if self.action == "list":
            return IssueListSerializer
        return super().get_serializer_class()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticated, (IsAdminUser | IsAuthorOrContributor)]

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs["issue_pk"])

    def perform_create(self, serializer):
        issue = Issue.objects.get(pk=self.kwargs["issue_pk"])
        serializer.save(author=self.request.user, issue=issue)

    def get_serializer_class(self):
        if self.action == "list":
            return CommentListSerializer
        return super().get_serializer_class()
