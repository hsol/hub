from django.urls import path, include

from community.views import (
    CommunityHomeView,
    CommunityMyPageView,
    CommunityProfileListView,
    CommunityProfileView,
    CommunityThreadListView,
)

urlpatterns = [
    path(
        "<int:community_id>",
        include(
            [
                path("", CommunityHomeView.as_view(), name="comm_home"),
                path("/me", CommunityMyPageView.as_view(), name="comm_mypage"),
                path(
                    "/profiles",
                    include(
                        [
                            path(
                                "",
                                CommunityProfileListView.as_view(),
                                name="comm_profiles",
                            ),
                            path(
                                "/<int:profile_id>",
                                CommunityProfileView.as_view(),
                                name="comm_profile",
                            ),
                        ]
                    ),
                ),
                path(
                    "/threads",
                    include(
                        [
                            path(
                                "",
                                CommunityThreadListView.as_view(),
                                name="comm_threads",
                            )
                        ]
                    ),
                ),
            ]
        ),
    ),
]
