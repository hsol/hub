from django.urls import path, include

from social.views import SocialThreadViewSet, SocialCommentViewSet

urlpatterns = [
    path(
        "api",
        include(
            [
                path(
                    "/threads",
                    include(
                        [
                            path(
                                "",
                                SocialThreadViewSet.as_view({"post": "create"}),
                            ),
                            path(
                                "/<int:pk>",
                                SocialThreadViewSet.as_view(
                                    {"patch": "partial_update", "delete": "destroy"}
                                ),
                            ),
                        ]
                    ),
                ),
                path(
                    "/comments",
                    include(
                        [
                            path(
                                "",
                                SocialCommentViewSet.as_view({"post": "create"}),
                            ),
                            path(
                                "/<int:pk>",
                                SocialCommentViewSet.as_view(
                                    {"put": "update", "delete": "destroy"}
                                ),
                            ),
                        ]
                    ),
                ),
            ]
        ),
    )
]
