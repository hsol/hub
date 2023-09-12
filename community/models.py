from django.contrib.auth.models import User
from django.db import models
from django_soft_delete.models import HasSoftDelete

from core.models import TimestampModel
from identify.models import Profile
from social.models import SocialThread, SocialThreadModel


class Community(SocialThreadModel, HasSoftDelete, TimestampModel):
    name = models.CharField(verbose_name="커뮤니티 이름", max_length=720, db_index=True)
    banner_img_url = models.URLField(
        verbose_name="배너 이미지 url",
        max_length=256,
        blank=True,
        default="https://picsum.photos/900/292",
    )

    owner = models.ForeignKey(
        User,
        verbose_name="커뮤니티 소유자",
        on_delete=models.DO_NOTHING,
        related_name="own_communities",
    )
    managers = models.ManyToManyField(
        User,
        verbose_name="관리자 목록",
        blank=True,
        related_name="in_charged_communities",
    )
    members = models.ManyToManyField(
        User,
        verbose_name="멤버 목록",
        blank=True,
        related_name="belong_communities",
    )

    class Meta:
        db_table = "community"
        verbose_name = "커뮤니티"
        verbose_name_plural = "커뮤니티 목록"

    def __str__(self):
        return self.name


class CommunityProfile(HasSoftDelete, TimestampModel):
    community = models.ForeignKey(
        Community,
        verbose_name="커뮤니티",
        related_name="profiles",
        on_delete=models.CASCADE,
    )
    profile = models.ForeignKey(
        Profile,
        verbose_name="프로필 정보",
        on_delete=models.CASCADE,
        related_name="community_through",
    )

    class Meta:
        db_table = "community_to_profile"
        verbose_name = "커뮤니티 프로필"
        verbose_name_plural = "커뮤니티 프로필 목록"

        unique_together = ["community", "profile"]

    def __str__(self):
        return f"{self.community.name} | {self.profile}"
