# Generated by Django 4.2.5 on 2023-09-11 02:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("identify", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("social", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Community",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="생성일자"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="수정일자"
                    ),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(
                        blank=True, default=None, null=True, verbose_name="Deleted At"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True, max_length=128, verbose_name="커뮤니티 이름"
                    ),
                ),
                (
                    "banner_img_url",
                    models.URLField(
                        blank=True,
                        default="",
                        max_length=256,
                        verbose_name="배너 이미지 url",
                    ),
                ),
                (
                    "managers",
                    models.ManyToManyField(
                        blank=True,
                        related_name="in_charged_communities",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="관리자 목록",
                    ),
                ),
                (
                    "members",
                    models.ManyToManyField(
                        blank=True,
                        related_name="belong_communities",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="멤버 목록",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="own_communities",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="커뮤니티 소유자",
                    ),
                ),
                (
                    "thread",
                    models.OneToOneField(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="social.socialthread",
                        verbose_name="스레드",
                        editable=False,
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "커뮤니티",
                "verbose_name_plural": "커뮤니티 목록",
                "db_table": "community",
            },
        ),
        migrations.CreateModel(
            name="CommunityProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="생성일자"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="수정일자"
                    ),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(
                        blank=True, default=None, null=True, verbose_name="Deleted At"
                    ),
                ),
                (
                    "community",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profiles",
                        to="community.community",
                        verbose_name="커뮤니티",
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="identify.profile",
                        verbose_name="프로필 정보",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
