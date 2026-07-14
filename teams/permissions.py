from rest_framework.permissions import BasePermission

from .models import Team, TeamMember


class IsOwner(BasePermission):
    """
    Allows only team owners to perform certain actions.
    """

    def has_object_permission(self, request, view, obj):
        # DRF browsable API may pass a TeamMember instance while rendering
        if isinstance(obj, TeamMember):
            team = obj.team
        elif isinstance(obj, Team):
            team = obj
        else:
            return False

        return TeamMember.objects.filter(
            team=team,
            user=request.user,
            role=TeamMember.Role.OWNER,
        ).exists()