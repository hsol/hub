from django.contrib.auth.models import User
from django.db import models, transaction
from django_soft_delete.models import HasSoftDelete
from phonenumber_field.modelfields import PhoneNumberField

from core.models import TimestampModel
from social.models import SocialThreadModel


class Profile(SocialThreadModel, HasSoftDelete, TimestampModel):
    owner = models.ForeignKey(
        User,
        verbose_name="소유자",
        on_delete=models.DO_NOTHING,
        related_name="own_profiles",
    )

    profile_img_url = models.URLField(
        verbose_name="프로필 이미지 URL",
        max_length=720,
        blank=True,
        default="https://picsum.photos/340/189",
    )

    last_name = models.CharField(verbose_name="성", max_length=8)
    first_name = models.CharField(verbose_name="이름", max_length=16)

    org_name = models.CharField(
        verbose_name="소속명", max_length=32, blank=True, default=""
    )
    job_title = models.CharField(
        verbose_name="직함", max_length=32, blank=True, default=""
    )

    phone_number = PhoneNumberField(verbose_name="휴대전화번호", blank=True, default="")
    email = models.EmailField(verbose_name="이메일주소", blank=True, default="")

    is_representative = models.BooleanField(
        verbose_name="대표 프로필 여부", default=False, db_index=True
    )

    class Meta:
        db_table = "profile"
        verbose_name = "프로필"
        verbose_name_plural = "프로필 목록"

        index_together = ["org_name", "job_title"]

    def get_full_name(self):
        return f"{self.last_name}{self.first_name}"

    @property
    def full_name(self):
        return self.get_full_name()

    def __str__(self):
        return self.full_name

    @transaction.atomic()
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        instance: Profile = super().save(
            force_insert, force_update, using, update_fields
        )
        instance.thread.owner = self.owner
        instance.thread.save(update_fields=["owner"])

        return instance
