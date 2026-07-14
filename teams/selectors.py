from .models import Team, TeamMember


def get_user_teams(user):
    return Team.objects.filter(
        members__user=user
    ).distinct()


def get_team_members(team):
    return TeamMember.objects.filter(
        team=team
    ).select_related("user")