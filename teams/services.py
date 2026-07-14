from .models import Team, TeamMember


def create_team(*, name, description, creator):
    """
    Creates a team and automatically assigns the creator
    as the OWNER.
    """

    team = Team.objects.create(
        name=name,
        description=description,
        created_by=creator,
    )

    TeamMember.objects.create(
        team=team,
        user=creator,
        role=TeamMember.Role.OWNER,
    )

    return team