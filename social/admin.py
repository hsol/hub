from django.contrib import admin

from social.models import SocialThread, SocialComment


@admin.register(SocialComment)
class SocialCommentAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]


class SocialCommentInline(admin.StackedInline):
    model = SocialComment
    extra = 0

    exclude = ["created_at", "updated_at", "deleted_at"]


@admin.register(SocialThread)
class SocialThreadAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]

    inlines = [SocialCommentInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["owner"].initial = request.user
        return form
