from django.db import models

from teams.models import Team


class Project(models.Model):
    name = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="projects",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name