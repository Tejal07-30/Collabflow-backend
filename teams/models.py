from django.conf import settings
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_teams"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
        
class TeamMember(models.Model):

    class Role(models.TextChoices):
        OWNER = "OWNER", "Owner"
        MAINTAINER = "MAINTAINER", "Maintainer"
        MEMBER = "MEMBER", "Member"
        VIEWER = "VIEWER", "Viewer"

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="members"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="team_memberships"
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("team", "user")

    def __str__(self):
        return f"{self.user.email} - {self.team.name}"