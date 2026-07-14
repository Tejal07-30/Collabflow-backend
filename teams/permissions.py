from rest_framework.permissions import BasePermission


class IsTeamOwner(BasePermission):
    """
    Allows access only to the team owner.
    """

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user