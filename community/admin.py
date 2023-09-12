from django.contrib import admin

from community.models import Community, CommunityProfile


class CommunityProfileAdmin(admin.TabularInline):
    model = CommunityProfile

    exclude = ["deleted_at"]
    extra = 0


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    autocomplete_fields = ["managers", "members"]

    exclude = ["created_at", "updated_at", "deleted_at"]
    inlines = [CommunityProfileAdmin]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["owner"].initial = request.user
        return form
