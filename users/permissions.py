from rest_framework.permissions import BasePermission


class SelfResourceAccess(BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action == 'create':
            return True

        return (request.user and request.user.is_authenticated and obj.id ==
                request.user.id)