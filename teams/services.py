from .models import Team, TeamMember
from django.contrib.auth import get_user_model

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


User = get_user_model()
def invite_member(*, team, email, role):
    """
    Adds an existing user to a team.
    """

    user = User.objects.filter(email=email).first()

    if not user:
        raise ValueError("User not found.")

    if TeamMember.objects.filter(team=team, user=user).exists():
        raise ValueError("User is already a member of this team.")

    member = TeamMember.objects.create(
        team=team,
        user=user,
        role=role,
    )

    return member