from rest_framework import permissions
from rest_framework.permissions import BasePermission

from projects.models import Project, Issue, Contributor, Comment


class IsAuthorOrContributor(BasePermission):

    def has_permission(self, request, view):
        if 'project_pk' in view.kwargs:
            return Contributor.objects.filter(user=request.user, project=view.kwargs[
                'project_pk']).exists()
        return True

    def has_object_permission(self, request, view, obj):
        if request.user and obj.author == request.user:
            return True
        if request.method in permissions.SAFE_METHODS:
            if isinstance(obj, Project):
                project = obj
            elif isinstance(obj, Issue):
                project = obj.project
            elif isinstance(obj, Comment):
                project = obj.issue.project
            else:
                return False

            return bool(request.user and Contributor.objects.filter(
                user=request.user, project=project).exists())

        return False
