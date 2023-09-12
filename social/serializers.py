from rest_framework.serializers import ModelSerializer

from social.models import SocialThread, SocialComment


class SocialThreadSerializer(ModelSerializer):
    class Meta:
        model = SocialThread
        fields = ["body", "owner"]


class SocialCommentSerializer(ModelSerializer):
    class Meta:
        model = SocialComment
        fields = ["thread", "body", "owner"]
