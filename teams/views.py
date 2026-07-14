from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Team
from .serializers import TeamSerializer
from .services import create_team


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Team.objects.filter(
            members__user=self.request.user
        ).distinct()

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