from autoslug import AutoSlugField
from django.db import models
from slugify import slugify

from core.models import TimestampModel


class Tag(TimestampModel):
    text = models.CharField(max_length=32, db_index=True)
    slug = AutoSlugField(populate_from="text", slugify=slugify)

    class Meta:
        verbose_name = "태그"
        verbose_name_plural = "태그목록"

        db_table = "tag"

    def __str__(self):
        return self.text
