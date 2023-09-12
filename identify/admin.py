from django.contrib import admin

from identify.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at", "deleted_at"]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["owner"].initial = request.user
        form.base_fields["last_name"].initial = request.user.last_name
        form.base_fields["first_name"].initial = request.user.first_name
        form.base_fields["email"].initial = request.user.email
        return form
