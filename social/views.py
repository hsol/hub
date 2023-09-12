from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from social.models import SocialThread, SocialComment
from social.serializers import SocialThreadSerializer, SocialCommentSerializer


class ThreadOwnerPermission(BasePermission):
    def has_object_permission(self, request: Request, view, obj: SocialThread):
        if not request.user.is_authenticated:
            return False

        if view.action in ["update", "partial_update", "destroy"]:
            return obj.owner == request.user


class CommentOwnerPermission(BasePermission):
    def has_object_permission(self, request: Request, view, obj: SocialComment):
        if not request.user.is_authenticated:
            return False

        if view.action in ["update", "partial_update", "destroy"]:
            return obj.owner == request.user


class SocialThreadViewSet(ModelViewSet):
    queryset = SocialThread.objects.prefetch_related(
        "owner__own_profiles",
        "comments__owner__own_profiles",
        "tags",
    )
    serializer_class = SocialThreadSerializer
    permission_classes = [ThreadOwnerPermission]

    def get_serializer(self, *args, **kwargs):
        kwargs["data"]["owner"] = self.request.user.id
        return super().get_serializer(*args, **kwargs)


class SocialCommentViewSet(ModelViewSet):
    queryset = SocialComment.objects.prefetch_related(
        "owner__own_profiles",
        "tags",
    )
    serializer_class = SocialCommentSerializer
    permission_classes = [CommentOwnerPermission]

    def get_serializer(self, *args, **kwargs):
        kwargs["data"]["owner"] = self.request.user.id
        return super().get_serializer(*args, **kwargs)
