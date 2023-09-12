from django.contrib import admin
from django.urls import path, include

from core.views import (
    IndexView,
    LoginView,
    EmailVerifyView,
    NeedToVerifyView,
    LogoutView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("community/", include("community.urls")),
    path("social/", include("social.urls")),
    path(
        "accounts/",
        include(
            [
                path("login/", LoginView.as_view(), name="login"),
                path("logout/", LogoutView.as_view(), name="logout"),
                path(
                    "need-to-verify/", NeedToVerifyView.as_view(), name="need_to_verify"
                ),
                path("verify/", EmailVerifyView.as_view(), name="verify"),
            ]
        ),
    ),
    path("", IndexView.as_view(), name="index"),
]
