from django.db import models
from django.contrib.auth.models import AbstractUser


class TimestampModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name="생성일자", auto_now_add=True, db_index=True
    )
    updated_at = models.DateTimeField(verbose_name="수정일자", auto_now=True, db_index=True)

    class Meta:
        abstract = True
