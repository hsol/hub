from django.contrib.auth.models import User
from django.db import models, transaction
from django.utils.text import Truncator
from django_soft_delete.models import HasSoftDelete

from core.models import TimestampModel
from meta.models import Tag


class SocialThread(HasSoftDelete, TimestampModel):
    body = models.TextField(verbose_name="내용", blank=True, default="", db_index=True)
    owner = models.ForeignKey(
        User,
        verbose_name="소유자",
        on_delete=models.DO_NOTHING,
        related_name="own_threads",
        null=True,
    )
    tags = models.ManyToManyField(Tag, verbose_name="관련태그목록", blank=True)

    class Meta:
        db_table = "social_thread"
        verbose_name = "스레드"
        verbose_name_plural = "스레드 목록"

    def __str__(self):
        return (
            f"{Truncator(self.body).words(16, truncate='...')}"
            if self.body
            else "(내용없음)"
        )


class SocialComment(HasSoftDelete, TimestampModel):
    thread = models.ForeignKey(
        SocialThread,
        verbose_name="스레드",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    body = models.TextField(verbose_name="내용", blank=True, default="", db_index=True)
    owner = models.ForeignKey(
        User,
        verbose_name="소유자",
        on_delete=models.DO_NOTHING,
        related_name="own_comments",
    )
    tags = models.ManyToManyField(Tag, verbose_name="관련태그목록", blank=True)

    class Meta:
        db_table = "social_comment"
        verbose_name = "코멘트"
        verbose_name_plural = "코멘트 목록"

    def __str__(self):
        return (
            f"{Truncator(self.body).words(16, truncate='...')}"
            if self.body
            else "(내용없음)"
        )


class SocialThreadModel(models.Model):
    thread = models.OneToOneField(
        SocialThread,
        verbose_name="스레드",
        on_delete=models.CASCADE,
        blank=True,
        editable=False,
        null=True,
    )

    @transaction.atomic()
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)

        try:
            assert self.thread
        except (AssertionError, SocialThread.DoesNotExist):
            self.thread = SocialThread.objects.create()
            self.save(update_fields=["thread"])

    class Meta:
        abstract = True
