from rest_framework import serializers
from .models import Team, TeamMember


class TeamSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.email")

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "description",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "created_at",
            "updated_at",
        ]


class TeamMemberSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = TeamMember
        fields = [
            "id",
            "user",
            "role",
            "joined_at",
        ]
        
class InviteMemberSerializer(serializers.Serializer):
    email = serializers.EmailField()

    role = serializers.ChoiceField(
        choices=TeamMember.Role.choices,
        default=TeamMember.Role.MEMBER,
    )