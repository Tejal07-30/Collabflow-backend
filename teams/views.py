from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Team, TeamMember
from .serializers import TeamSerializer, TeamMemberSerializer, InviteMemberSerializer, UpdateRoleSerializer
from .services import create_team, invite_member, update_member_role, remove_team_member
from .selectors import get_user_teams, get_team_members
from .permissions import IsOwner

class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_user_teams(self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        team = create_team(
            name=serializer.validated_data["name"],
            description=serializer.validated_data.get("description", ""),
            creator=request.user,
        )

        response_serializer = self.get_serializer(team)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["get"])
    def members(self, request, pk=None):
        team = self.get_object()

        members = get_team_members(team)

        serializer = TeamMemberSerializer(
            members,
            many=True,
        )

        return Response(serializer.data)
    @action(detail=True, methods=["post"])
    def invite(self, request, pk=None):
        team = self.get_object()

        # Only owners can invite members
        self.check_object_permissions(request, team)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            member = invite_member(
                team=team,
                email=serializer.validated_data["email"],
                role=serializer.validated_data["role"],
            )
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            TeamMemberSerializer(member).data,
            status=status.HTTP_201_CREATED,
        )
    def get_permissions(self):
        if self.action == "invite":
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]

    def get_serializer_class(self):

        if self.action == "invite":
            return InviteMemberSerializer

        if self.action == "members":
            return TeamMemberSerializer

        if self.action == "change_role":
            return UpdateRoleSerializer

        return TeamSerializer

    @action(
        detail=True,
        methods=["patch"],
        url_path=r"members/(?P<member_id>\d+)/role",
    )
    def change_role(self, request, pk=None, member_id=None):

        team = self.get_object()

        self.check_object_permissions(request, team)

        serializer = UpdateRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            member = TeamMember.objects.get(
                id=member_id,
                team=team,
            )

            member = update_member_role(
                member=member,
                role=serializer.validated_data["role"],
            )

        except TeamMember.DoesNotExist:
            return Response(
                {"detail": "Member not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            TeamMemberSerializer(member).data
        )

    @action(
        detail=True,
        methods=["delete"],
        url_path=r"members/(?P<member_id>\d+)",
    )
    def remove_member(self, request, pk=None, member_id=None):

        team = self.get_object()

        self.check_object_permissions(request, team)

        try:
            member = TeamMember.objects.get(
                id=member_id,
                team=team,
            )

            remove_team_member(member=member)

        except TeamMember.DoesNotExist:
            return Response(
                {"detail": "Member not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Member removed successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )