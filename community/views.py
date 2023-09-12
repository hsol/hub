from functools import cached_property

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import BadRequest, PermissionDenied
from django.db.models import Prefetch, Q
from django.db.models.functions import Concat
from django.views.generic import TemplateView, RedirectView

from community.models import Community
from identify.models import Profile
from social.models import SocialComment


class CommunityContextMixin(LoginRequiredMixin, TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id is not None:
            if not self.request.user.own_profiles.filter(
                community_through__community_id=self.community_id
            ).exists():
                raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_permission_denied_message(self):
        return "커뮤니티에 가입되어있지 않습니다. 관리자에게 문의해주세요!"

    @cached_property
    def community_id(self):
        if community_id := self.kwargs.get("community_id"):
            return community_id

        raise BadRequest

    @property
    def community(self):
        return Community.objects.prefetch_related(
            "profiles",
            Prefetch(
                "thread__comments",
                SocialComment.objects.filter(
                    thread__community__id=self.community_id
                ).order_by("-created_at"),
            ),
            Prefetch(
                "managers__own_profiles",
                Profile.objects.filter(
                    community_through__community_id=self.community_id
                ).distinct(),
            ),
            Prefetch(
                "members__own_profiles",
                Profile.objects.filter(
                    community_through__community_id=self.community_id
                )
                .order_by(Concat("last_name", "first_name"))
                .distinct(),
            ),
        ).get(id=self.community_id)

    def get_context_data(self, community_id: int, **kwargs):
        context_data = super().get_context_data(**kwargs)

        return {
            **context_data,
            "community": self.community,
        }


class CommunityHomeView(CommunityContextMixin, TemplateView):
    template_name = "community/home.html"


class CommunityMyPageView(LoginRequiredMixin, RedirectView):
    pattern_name = "comm_profile"

    def get_redirect_url(self, *args, community_id: int, **kwargs):
        profile = self.request.user.own_profiles.get(
            community_through__community_id=community_id
        )

        return super().get_redirect_url(
            community_id=community_id, profile_id=profile.id
        )


class CommunityProfileListView(CommunityContextMixin, TemplateView):
    template_name = "community/profile_list.html"

    def get_context_data(self, *args, community_id: int = None, **kwargs):
        context_data = super().get_context_data(community_id=community_id, **kwargs)

        if q := self.request.GET.get("q"):
            profile_ids = (
                self.community.profiles.annotate(
                    full_name=Concat("profile__last_name", "profile__first_name")
                )
                .filter(
                    Q(full_name__icontains=q)
                    | Q(profile__org_name__icontains=q)
                    | Q(profile__job_title__icontains=q)
                )
                .values_list("profile_id", flat=True)
            )
        else:
            profile_ids = self.community.profiles.values_list("profile_id", flat=True)

        return {
            **context_data,
            "profiles": Profile.objects.filter(id__in=profile_ids)
            .order_by(Concat("last_name", "first_name"))
            .select_related("thread")
            .distinct(),
        }


class CommunityProfileView(CommunityContextMixin, TemplateView):
    template_name = "community/profile_detail.html"

    def get_context_data(
        self, *args, community_id: int = None, profile_id: int = None, **kwargs
    ):
        context_data = super().get_context_data(community_id=community_id, **kwargs)

        return {
            **context_data,
            "profile": Profile.objects.prefetch_related(
                Prefetch(
                    "thread__comments",
                    SocialComment.objects.order_by("-created_at").prefetch_related(
                        Prefetch(
                            "owner__own_profiles",
                            Profile.objects.filter(
                                community_through__community_id=community_id
                            ),
                        )
                    ),
                ),
            ).get(id=profile_id, community_through__community_id=community_id),
        }


class CommunityThreadListView(CommunityContextMixin, TemplateView):
    template_name = "community/thread_list.html"
